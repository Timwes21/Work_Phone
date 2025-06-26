import json

SYSTEM_MESSAGE = (
    "You are an AI Assistant that is called when the user has a missed call."
    "You are to either schedule a callback, pass a message, or answer any quesions"
    "The caller may have. Ask for Their name, at some point, but do not interupt."
    "Only say one sentence at a time so you dont interupt them."
)
VOICE = 'alloy'

async def send_initial_conversation_item(openai_ws):
    """Send initial conversation item if AI talks first."""
    initial_conversation_item = {
        "type": "conversation.item.create",
        "item": {
            "type": "message",
            "role": "user",
            "content": [
                {
                    "type": "input_text",
                    "text": "Greet the user with 'Hello there! Sorry Tim did not pick up but i can answer any questions or schedule a callback wht tim himself'"
                }
            ],
            
        }
    }
    await openai_ws.send(json.dumps(initial_conversation_item))
    await openai_ws.send(json.dumps({"type": "response.create"}))


async def initialize_session(openai_ws, name):
    """Control initial session with OpenAI."""
    session_update = {
        "type": "session.update",
        "session": {
            "turn_detection": {"type": "server_vad"},
            "input_audio_format": "g711_ulaw",
            "output_audio_format": "g711_ulaw",
            "voice": VOICE,
            "instructions": SYSTEM_MESSAGE,
            "modalities": ["text", "audio"],
            "temperature": 0.8,
            "input_audio_transcription": {
                "model": "gpt-4o-transcribe",
            },
            "tools": [{
                "type": "function",
                "name": "query_documents",
                "description": "If the caller is asking about something that pertains the person they were trying to call, then this function will be called",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "what you need to be able to query for the semantic search of the documents",
                        }
                    },
                    "required": ["query"]
                }
            },
            {
                "type": "function",
                "name": "schedule_callback",
                "description": f"If the caller is wanting to schedule a callback with {name}",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "date": {
                            "type": "string",
                            "description": f"the date that the caller wants {name} to call them back",
                        },
                        "time": {
                            "type": "string",
                            "description": f"the date that the caller wants {name} to call them back"
                        }
                    },
                    "required": ["date", "time"]
                }
            }
        ],
        "tool_choice": "auto",
        }
    }
    print('Sending session update:', json.dumps(session_update))
    await openai_ws.send(json.dumps(session_update))

    # Uncomment the next line to have the AI speak first
    await send_initial_conversation_item(openai_ws)