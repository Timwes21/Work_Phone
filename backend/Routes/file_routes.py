from fastapi import APIRouter, Request, Form, UploadFile
from fastapi.responses import JSONResponse
from utils.db import collection
import docx
import pdfplumber
import io
import json


router = APIRouter()

@router.post("/save-files/{number}")
async def save_files(number: str, file: UploadFile = Form(...)):
    ext = file.headers['content-type']
    file_name = file.filename
    res = collection.find_one({"number": number})
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
    
    collection.update_one({"number": number},{"$push": {"files": {file_name: contents}}})
    
    
    
    

    
@router.get("/get-files/{number}", response_class=JSONResponse)
async def get_files(number: str):
    user = collection.find_one({"number": number})
    files = [j for i in user["files"] for j in i.keys()]
    print(files)
    return {"files": files}

@router.post("/delete-file/{number}")
async def delete_file(request: Request, number: str):
    body: bytes = await request.body()
    body: str = body.decode()
    body = json.loads(body)
    print(body)
    
    file_name = body["filename"]
    account = collection.find_one({"number": number})
    files: list = account["files"]
    n = 0
    for i in files:
        if file_name in i.keys():
            break    
        n+=1
    files.pop(n)
    collection.update_one({"number": number},{"$set": {"files": files}})
    return "Succes"
