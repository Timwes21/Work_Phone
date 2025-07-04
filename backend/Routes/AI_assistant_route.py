from fastapi import APIRouter, WebSocket, Request
from utils.call_choice import dial_agent, dial_person
from utils.query import ask_document
from utils.db import collection
from init_session import initialize_session
from utils.openaiws import RealTimeInteraction
from langchain.chains.retrieval_qa.base import BaseRetrievalQA
import os, certifi
os.environ["OPENAI_CA_BUNDLE"] = certifi.where()
import websockets
import asyncio
import os
import json
import base64

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
    # results = await collection.find_one({"number": business_number})
    # name = results['name']
    return dial_agent(request, business_number)

@router.post("/get-call-status")
async def call_status(request: Request):
    print("***In get-call-status route**")
    body: bytes = await request.body()
    body: str = body.decode()
    body = {i.split("=")[0]: i.split("=")[1] for i in body.split("&")}
        
    
    if body["DialCallStatus"] != "completed":
        return dial_agent(request)
    

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
    # await websocket.accept()
    # async with websockets.connect(
    #     'wss://api.openai.com/v1/realtime?model=gpt-4o-realtime-preview-2024-10-01',
    #     extra_headers={
    #         "Authorization": f"Bearer {OPENAI_API_KEY}",
    #         "OpenAI-Beta": "realtime=v1"
    #     }
    # ) as openai_ws:
    #     call_log = []
    #     qa = await ask_document(business_number)
        
    #     await initialize_session(openai_ws)

    #     # Connection specific state
    #     stream_sid = None
    #     latest_media_timestamp = 0
    #     last_assistant_item = None
    #     mark_queue = []
    #     response_start_timestamp_twilio = None
        
    #     async def receive_from_twilio():
    #         """Receive audio data from Twilio and send it to the OpenAI Realtime API."""
    #         nonlocal stream_sid, latest_media_timestamp
    #         try:
    #             async for message in websocket.iter_text():
    #                 data = json.loads(message)
    #                 if data['event'] == 'media' and openai_ws.open:
    #                     latest_media_timestamp = int(data['media']['timestamp'])
    #                     audio_append = {
    #                         "type": "input_audio_buffer.append",
    #                         "audio": data['media']['payload']
    #                     }
    #                     await openai_ws.send(json.dumps(audio_append))
                        
    #                 elif data['event'] == 'start':
    #                     stream_sid = data['start']['streamSid']
    #                     print(f"Incoming stream has started {stream_sid}")
    #                     response_start_timestamp_twilio = None
    #                     latest_media_timestamp = 0
    #                     last_assistant_item = None
                        
    #                 elif data['event'] == 'mark':
    #                     if mark_queue:
    #                         mark_queue.pop(0)
    #                 elif data["event"] == "done":
    #                     pass
    #         except WebSocketDisconnect:
    #             print("Client disconnected.")
    #             if openai_ws.open:
    #                 await openai_ws.close()

    #     async def send_to_twilio():
    #         """Receive events from the OpenAI Realtime API, send audio back to Twilio."""
    #         nonlocal stream_sid, last_assistant_item, response_start_timestamp_twilio, call_log
    #         try:
    #             async for openai_message in openai_ws:
    #                 response = json.loads(openai_message)
    #                 if response['type'] in LOG_EVENT_TYPES:
    #                     # print(f"Received event: {response['type']}", response)
    #                     pass

    #                 if response.get('type') == 'response.audio.delta' and 'delta' in response:
    #                     audio_payload = base64.b64encode(base64.b64decode(response['delta'])).decode('utf-8')
    #                     audio_delta = {
    #                         "event": "media",
    #                         "streamSid": stream_sid,
    #                         "media": {
    #                             "payload": audio_payload
    #                         }
    #                     }
    #                     await websocket.send_json(audio_delta)

    #                     if response_start_timestamp_twilio is None:
    #                         response_start_timestamp_twilio = latest_media_timestamp
    #                         if SHOW_TIMING_MATH:
    #                             print(f"Setting start timestamp for new response: {response_start_timestamp_twilio}ms")

    #                     # Update last_assistant_item safely
    #                     if response.get('item_id'):
    #                         last_assistant_item = response['item_id']

    #                     await send_mark(websocket, stream_sid)

    #                 # Trigger an interruption. Your use case might work better using `input_audio_buffer.speech_stopped`, or combining the two.
    #                 if response.get('type') == 'input_audio_buffer.speech_started':
    #                     print("Speech started detected.")
    #                     if last_assistant_item:
    #                         print(f"Interrupting response with id: {last_assistant_item}")
    #                         await handle_speech_started_event()
                            
    #                 if response.get("type") == 'conversation.item.input_audio_transcription.completed':  
    #                     user_input = response["transcript"]
    #                     call_log += [{"caller": user_input}]
                        
                        
    #                 if response.get("type") == 'response.audio_transcript.done':
    #                     AI_response = response["transcript"]
    #                     call_log += [{"AI": AI_response}]
                        
    #                 if response.get("type") == "response.done":
    #                     response = response['response']["output"]
    #                     if len(response) > 0:
    #                         response = response[0]
    #                         if response['type'] == "function_call":
    #                             query: BaseRetrievalQA = response['arguments']                                
    #                             results = qa.invoke(query)
    #                             results = results['result']
    #                             send_results = {
    #                                 "type": "conversation.item.create",
    #                                 "item": {
    #                                     "type": "function_call_output",
    #                                     "call_id": response["id"],
    #                                     "output": "{\"query_results\": \"" + results + "\"}"
    #                                 }
    #                             }
    #                             openai_ws.send(json.dumps(send_results))

    #                     else:
    #                         print("empty list")
                        
    #                     # response = response['response']["output"][0]
    #                     # if response["type"] == "function_call":
    #                         # print(response["name"])
                            
                    
    #         except Exception as e:
    #             print(f"Error in send_to_twilio: {e}")

    #     async def handle_speech_started_event():
    #         """Handle interruption when the caller's speech starts."""
    #         nonlocal response_start_timestamp_twilio, last_assistant_item
    #         print("Handling speech started event.")
    #         if mark_queue and response_start_timestamp_twilio is not None:
    #             elapsed_time = latest_media_timestamp - response_start_timestamp_twilio
    #             if SHOW_TIMING_MATH:
    #                 print(f"Calculating elapsed time for truncation: {latest_media_timestamp} - {response_start_timestamp_twilio} = {elapsed_time}ms")

    #             if last_assistant_item:
    #                 if SHOW_TIMING_MATH:
    #                     print(f"Truncating item with ID: {last_assistant_item}, Truncated at: {elapsed_time}ms")

    #                 truncate_event = {
    #                     "type": "conversation.item.truncate",
    #                     "item_id": last_assistant_item,
    #                     "content_index": 0,
    #                     "audio_end_ms": elapsed_time
    #                 }
    #                 await openai_ws.send(json.dumps(truncate_event))

    #             await websocket.send_json({
    #                 "event": "clear",
    #                 "streamSid": stream_sid
    #             })

    #             mark_queue.clear()
    #             last_assistant_item = None
    #             response_start_timestamp_twilio = None

    #     async def send_mark(connection, stream_sid):
    #         if stream_sid:
    #             mark_event = {
    #                 "event": "mark",
    #                 "streamSid": stream_sid,
    #                 "mark": {"name": "responsePart"}
    #             }
    #             await connection.send_json(mark_event)
    #             mark_queue.append('responsePart')

    #     await asyncio.gather(receive_from_twilio(), send_to_twilio())
