from fastapi import APIRouter, Request, Form, UploadFile
from fastapi.responses import JSONResponse
from utils.query import save_docs_with_faiss
from utils.file_parse import get_doc_contents




router = APIRouter()

async def get_list(items: list):
    for index, value in enumerate(items):
        yield index, value

async def get_dict(items: dict):
    for key, value in items.items():
        yield key, value

@router.post("/save-files", response_class=JSONResponse)
async def save_files(request: Request, file: UploadFile = Form(...), token: str = Form(...)):
    collection = request.app.state.collection
    file_name = file.filename
    current = request.app.state.decode_access_token(token)
    
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
    
    
    
    

    
@router.get("/get-files", response_class=JSONResponse)
async def get_files(request: Request):
    token = request.headers["token"]
    token = request.app.state.decode_token(token)
    collection = request.app.state.collection
    user = await collection.find_one({"tokens": token})
    files = user['files']
    file_names = [file_name async for _,file in get_list(files) async for file_name,_ in get_dict(file)]
    print(file_names)
    return {"files": file_names}

@router.post("/delete-file")
async def delete_file(request: Request):
    data = await request.app.state.get_data(request)
    collection = request.app.state.collection
    file_name = data["filename"]
    user_account = await collection.find_one({"tokens": data["token"]}) or {}
    files: list[dict] = user_account.get("files", [])
    
    async for index, value in get_list(files):
        if file_name in value.keys():
            files.pop(index)    
            break


    all_files_contents = [k async for _, i in get_list(files) async for _, k in get_dict(i)]
    await save_docs_with_faiss(all_files_contents, user_account.get('twilio_number', ""))
    await collection.update_one({"tokens": data['token']},{"$set": {"files": files}})
    return "Success"
