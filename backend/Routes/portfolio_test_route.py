from fastapi import APIRouter, Form, UploadFile, Request, WebSocket
from utils.db import collection
from utils.file_parse import get_doc_contents
from utils.query import save_docs_with_faiss
from utils.call_choice import dial_agent
from utils.openaiws import RealTimeInteraction
import os

OPENAI_API_KEY = os.getenv('OPENAI_KEY')


router = APIRouter()

@router.post("/test")
async def test(name: str = Form(...), file: UploadFile = Form(...)):
    contents_of_file: dict = await get_doc_contents(file)
    await save_docs_with_faiss(contents_of_file, "7726771701", portfolio=True)

    await collection.update_one({"twilio_number": "+17726771701"}, {"$set": {"files": contents_of_file, "name": name}})
    return "Updated!"

@router.api_route("/incoming-call/{business_number}", methods=["GET", "POST"])
async def handle_incoming_call(request: Request, business_number: str):
    print("***in incoming-call route***")
    return await dial_agent(request, business_number, "portfolio")

@router.websocket("/media-stream/{business_number}")
async def handle_media_stream(websocket: WebSocket, business_number: str):
    """Handle WebSocket connections between Twilio and OpenAI."""
    print("Client connected")

    headers={
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "OpenAI-Beta": "realtime=v1"
    }

    ws_convo = RealTimeInteraction(websocket, headers)
    await ws_convo.start(business_number)
