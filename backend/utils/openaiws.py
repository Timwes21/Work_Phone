import json
import websockets
import base64
from fastapi.websockets import WebSocketDisconnect
import asyncio
from utils.query import ask_document
from init_session import initialize_session
import os
from dotenv import load_dotenv
load_dotenv()


class RealTimeInteraction:
    url = 'wss://api.openai.com/v1/realtime?model=gpt-4o-realtime-preview-2024-10-01'
    LOG_EVENT_TYPES = [
    'error', 'response.content.done', 'rate_limits.updated',
    'response.done', 'input_audio_buffer.committed',
    'input_audio_buffer.speech_stopped', 'input_audio_buffer.speech_started',
    'session.created', 'response.create'
    ]
    
    
    def __init__(self, ws, headers):
        self.ws = ws
        self.headers = headers
        self.call_log = []
        self.stream_sid = None
        self.latest_media_timestamp = 0
        self.last_assistant_item = None
        self.mark_queue = []
        self.response_start_timestamp_twilio = None
        self.SHOW_TIMING_MATH = False    

    async def start(self, business_number):
        await self.ws.accept()
        async with websockets.connect(self.url, extra_headers=self.headers) as openai_ws:
            print(openai_ws)
            self.openai_ws = openai_ws
            print(self.openai_ws)
            self.qa = await ask_document(business_number)
        
            await initialize_session(self.openai_ws, self.qa)
            await asyncio.gather(self.receive_from_twilio(), self.send_to_twilio())

 
    
    async def receive_from_twilio(self):
        print("****in recieve_from_twilio****")
        #         nonlocal stream_sid, latest_media_timestamp
        """Receive audio data from Twilio and send it to the OpenAI Realtime API."""
        try:
            async for message in self.ws.iter_text():
                data = json.loads(message)
                if data['event'] == 'media' and self.openai_ws.open:
                    self.latest_media_timestamp = int(data['media']['timestamp'])
                    audio_append = {
                        "type": "input_audio_buffer.append",
                        "audio": data['media']['payload']
                    }
                    await self.openai_ws.send(json.dumps(audio_append))
                    
                elif data['event'] == 'start':
                    self.stream_sid = data['start']['streamSid']
                    print(f"Incoming stream has started {self.stream_sid}")
                    self.response_start_timestamp_twilio = None
                    self.latest_media_timestamp = 0
                    self.last_assistant_item = None
                    
                elif data['event'] == 'mark':
                    if self.mark_queue:
                        self.mark_queue.pop(0)
                elif data["event"] == "done":
                    pass
        except WebSocketDisconnect:
            print("Client disconnected.")
            if self.openai_ws.open:
                await self.openai_ws.close()

    async def send_to_twilio(self):
#         nonlocal stream_sid, last_assistant_item, response_start_timestamp_twilio, call_log
        print("****in send_to_twilio****")
        """Receive events from the OpenAI Realtime API, send audio back to Twilio."""
        try:
            async for openai_message in self.openai_ws:
                response = json.loads(openai_message)
                if response['type'] in self.LOG_EVENT_TYPES:
                    print(f"Received event: {response['type']}", response)
                    pass

                if response.get('type') == 'response.audio.delta' and 'delta' in response:
                    audio_payload = base64.b64encode(base64.b64decode(response['delta'])).decode('utf-8')
                    audio_delta = {
                        "event": "media",
                        "streamSid": self.stream_sid,
                        "media": {
                            "payload": audio_payload
                        }
                        }
                    await self.ws.send_json(audio_delta)

                    if self.response_start_timestamp_twilio is None:
                        self.response_start_timestamp_twilio = self.latest_media_timestamp
                        if self.SHOW_TIMING_MATH:
                            print(f"Setting start timestamp for new response: {self.response_start_timestamp_twilio}ms")

                    # Update last_assistant_item safely
                    if response.get('item_id'):
                        self.last_assistant_item = response['item_id']

                    await self.send_mark(self.ws, self.stream_sid)

                # Trigger an interruption. Your use case might work better using `input_audio_buffer.speech_stopped`, or combining the two.
                if response.get('type') == 'input_audio_buffer.speech_started':
                    print("Speech started detected.")
                    if self.last_assistant_item:
                        print(f"Interrupting response with id: {self.last_assistant_item}")
                        await self.handle_speech_started_event()
                        
                # if response.get("type") == 'conversation.item.input_audio_transcription.completed':  
                #     user_input = response["transcript"]
                #     self.call_log += [{"caller": user_input}]
                    
                    
                # if response.get("type") == 'response.audio_transcript.done':
                #     AI_response = response["transcript"]
                #     self.call_log += [{"AI": AI_response}]
                    
                if response.get("type") == "response.done":
                    response = response['response']["output"]
                    if len(response) > 0:
                        response = response[0]
                        if response['type'] == "function_call":
                            query = response['arguments']                                
                            results = await self.qa.ainvoke(query)
                            results = results['result']
                            print(results)
                            send_results = {
                                "type": "conversation.item.create",
                                "item": {
                                    "type": "function_call_output",
                                    "call_id": response["call_id"],
                                    "output": "{\"query_results\": \"" + results + "\"}"
                                }
                            }
                            await self.openai_ws.send(json.dumps(send_results))
                            await self.openai_ws.send(json.dumps({"type": "response.create"}))

                    else:
                        print("empty list")
                    
                    # response = response['response']["output"][0]
                    # if response["type"] == "function_call":
                        # print(response["name"])
                        
                
        except Exception as e:
            print(f"Error in send_to_twilio: {e}")

    async def handle_speech_started_event(self):
        """Handle interruption when the caller's speech starts."""
        print("****Handling speech started event****")
        if self.mark_queue and self.response_start_timestamp_twilio is not None:
            elapsed_time = self.latest_media_timestamp - self.response_start_timestamp_twilio
            if self.SHOW_TIMING_MATH:
                print(f"Calculating elapsed time for truncation: {self.latest_media_timestamp} - {self.response_start_timestamp_twilio} = {elapsed_time}ms")

            if self.last_assistant_item:
                if self.SHOW_TIMING_MATH:
                    print(f"Truncating item with ID: {self.last_assistant_item}, Truncated at: {elapsed_time}ms")

                truncate_event = {
                    "type": "conversation.item.truncate",
                    "item_id": self.last_assistant_item,
                    "content_index": 0,
                    "audio_end_ms": elapsed_time
                }
                await self.openai_ws.send(json.dumps(truncate_event))

            await self.ws.send_json({
                "event": "clear",
                "streamSid": self.stream_sid
            })

            self.mark_queue.clear()
            self.last_assistant_item = None
            self.response_start_timestamp_twilio = None

    async def send_mark(self, connection, stream_sid):
        if stream_sid:
            mark_event = {
                "event": "mark",
                "streamSid": stream_sid,
                "mark": {"name": "responsePart"}
            }
            await connection.send_json(mark_event)
            self.mark_queue.append('responsePart')

