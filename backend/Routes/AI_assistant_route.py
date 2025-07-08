from fastapi import APIRouter, WebSocket, Request
from utils.call_choice import dial_agent, dial_person
from utils.query import ask_document
from utils.db import collection
from init_session import initialize_session
from utils.openaiws import RealTimeInteraction
from langchain.chains.retrieval_qa.base import BaseRetrievalQA
import os

OPENAI_API_KEY = os.getenv('OPENAI_KEY')

LOG_EVENT_TYPES = [
    'error', 'response.content.done', 'rate_limits.updated',
    'response.done', 'input_audio_buffer.committed',
    'input_audio_buffer.speech_stopped', 'input_audio_buffer.speech_started',
    'session.created'
]
SHOW_TIMING_MATH = False
router = APIRouter()


@router.api_route("/incoming-call/{business_number}", methods=["GET", "POST"])
async def handle_incoming_call(request: Request, business_number: str):
    print("***in incoming-call route***")
    await dial_person(business_number)

@router.post("/get-call-status/{business_number}")
async def call_status(request: Request, business_number: str):
    print("***In get-call-status route**")
    body: bytes = await request.body()
    body: str = body.decode()
    body = {i.split("=")[0]: i.split("=")[1] for i in body.split("&")}
        
    
    if body["DialCallStatus"] != "completed":
        return dial_agent(request, business_number, "ai-assistant")
    

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
    