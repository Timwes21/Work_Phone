from fastapi import APIRouter, WebSocket, Request
from utils.call_choice import dial_agent, dial_person
from utils.query import ask_document
from utils.openaiws import RealTimeInteraction
from langchain.chains.retrieval_qa.base import BaseRetrievalQA
import os

OPENAI_API_KEY = os.getenv('OPENAI_KEY')

router = APIRouter()


@router.api_route("/incoming-call/{twilio_number}", methods=["GET", "POST"])
async def handle_incoming_call(request: Request, twilio_number: str):
    print("***in incoming-call route***")
    user = await request.app.state.collection.find_one({"twilio_number": twilio_number})
    return await dial_person(twilio_number, "ai-assistant")

@router.post("/get-call-status/{twilio_number}")
async def call_status(request: Request, twilio_number: str):
    print("***In get-call-status route**")
    body: bytes = await request.body()
    body: str = body.decode()
    body = {i.split("=")[0]: i.split("=")[1] for i in body.split("&")}
        
    
    if body["DialCallStatus"] != "completed":
        return await dial_agent(request, twilio_number, "ai-assistant")
    

@router.websocket("/media-stream/{business_number}")
async def handle_media_stream(websocket: WebSocket, business_number: str):
    """Handle WebSocket connections between Twilio and OpenAI."""
    print("Client connected")

    headers={
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "OpenAI-Beta": "realtime=v1"
    }
    collection = websocket.app.state.collection
    ws_convo = RealTimeInteraction(websocket, headers)
    await ws_convo.start(business_number, collection)
    