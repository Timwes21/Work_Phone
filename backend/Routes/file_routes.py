from fastapi import APIRouter, Request, Form, UploadFile
from fastapi.responses import JSONResponse
from utils.db import collection
from utils.query import save_docs_with_faiss
from utils.access_token import decode_access_token
from utils.data import get_data
from utils.file_parse import get_doc_contents




router = APIRouter()

@router.post("/save-files", response_class=JSONResponse)
async def save_files(file: UploadFile = Form(...), token: str = Form(...)):
    print(file)
    file_name = file.filename
    current = decode_access_token(token)
    
    res = await collection.find_one({"tokens": current})
    existent_files = res['files']
    print(existent_files)    
    if file_name in existent_files:
        return {"file_exists": True}
    
    
    
    contents = await get_doc_contents(file)

    await save_docs_with_faiss([contents], res['twilio_number'])
    print("here")
    await collection.update_one({"tokens": current},{"$push": {"files": {file_name: contents}}})
    return {"file_exists": False}
    
    
    
    

    
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
    user_account = await collection.find_one({"tokens": data["token"]})
    files: list[dict] = user_account["files"]
    n = 0
    for i in files:
        if file_name in i.keys():
            break    
        n+=1
    files.pop(n)
    all_files_contents = [k for i in user_account['files'] for [_, k] in i.items()]

    await save_docs_with_faiss(all_files_contents, user_account['twilio_number'])
    await collection.update_one({"tokens": data['token']},{"$set": {"files": files}})
    return "Success"
