from fastapi import APIRouter, Form, UploadFile
from utils.db import collection
from utils.file_parse import get_doc_contents
from utils.query import save_docs


router = APIRouter()

@router.get("/test")
async def test(name: str = Form(...), number: str = Form(...), file: UploadFile = Form(...)):
    contents = await get_doc_contents(file)
    save_docs(contents, "7726771701")

    await collection.update_one({"number": "+17726771701"}, {"$set": {"files": contents, "name": name, "personal_number": number}})
    return "Updated!"
