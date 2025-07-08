from fastapi import APIRouter, Request, Form, UploadFile
from fastapi.responses import JSONResponse
from utils.db import collection
from utils.query import save_docs
from utils.access_token import decode_access_token
from utils.data import get_data
from pydantic import BaseModel
from utils.file_parse import get_doc_contents
import json




router = APIRouter()

@router.post("/save-files")
async def save_files(file: UploadFile = Form(...), token: str = Form(...)):
    print(file)
    file_name = file.filename
    current = decode_access_token(token)
    
    res = await collection.find_one({"tokens": current})
    existent_files = res['files']
    print(existent_files)    
    if file_name in existent_files:
        return "File Already Exists"
    
    
    
    contents = get_doc_contents(file)

    save_docs([contents], res['twilio_number'])
    
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
    files: list[dict] = account["files"]
    n = 0
    for i in files:
        if file_name in i.keys():
            break    
        n+=1
    files.pop(n)
    files = account['files']
    files_contents_dict = [k for i in files for [j, k] in i.items()]

    save_docs(files_contents_dict, account['number'])
    await collection.update_one({"tokens": data['token']},{"$set": {"files": files}})
    return "Success"
