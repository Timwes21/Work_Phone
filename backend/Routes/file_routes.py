from fastapi import APIRouter, Request, Form, UploadFile
from fastapi.responses import JSONResponse
from utils.db import collection
from utils.query import save_docs
from utils.access_token import decode_access_token
from utils.data import get_data
from pydantic import BaseModel
import docx
import pdfplumber
import io
import json




router = APIRouter()

@router.post("/save-files")
async def save_files(file: UploadFile = Form(...), token: str = Form(...)):
    print(file)
    ext = file.headers['content-type']
    file_name = file.filename
    current = decode_access_token(token)
    
    res = await collection.find_one({"tokens": current})
    existent_files = [j for i in res["files"] for j in i.keys()]
    print(existent_files)    
    if file_name in existent_files:
        return "File Already Exists"
    
    doc_bytes = await file.read()
    
    if "vnd.openxmlformats-officedocument.wordprocessingml.document" in ext:
        print("document is docx file")
        document = docx.Document(io.BytesIO(doc_bytes))
        contents = "\n".join([para.text for para in document.paragraphs])
    elif "pdf" in ext:
        print("document is pdf file")
        pdf = pdfplumber.open(io.BytesIO(doc_bytes))
        pages = pdf.pages
        contents = "\n".join([page.extract_text() for page in pages])

    save_docs(contents, res['number'])
    
    await collection.update_one({"tokens": current},{"$push": {"files": {file_name: contents}}})
    
    
    
    

    
@router.post("/get-files", response_class=JSONResponse)
async def get_files(request: Request):
    data = await get_data(request)
    user = await collection.find_one({"tokens": data["token"]})
    file_names = [j for i in user["files"] for j in i.keys()]
    print(file_names)
    return {"files": file_names}

@router.post("/delete-file")
async def delete_file(request: Request):
    data = await get_data(request)
    
    file_name = data["filename"]
    account = await collection.find_one({"tokens": data["token"]})
    files: list = account["files"]
    n = 0
    for i in files:
        if file_name in i.keys():
            break    
        n+=1
    files.pop(n)
    files = account['files']
    print("----made it pas the double for loop----")
    files_contents_list = [j for i in files for j in i.values()]

    save_docs(files_contents_list, account['number'])
    await collection.update_one({"tokens": data['token']},{"$set": {"files": files}})
    return "Success"
