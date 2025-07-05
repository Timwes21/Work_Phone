import json

SYSTEM_MESSAGE = (
    "You are an AI Assistant for Tim, for when someone calls him and he doesnt pick up, you are actiavted."
    "You're purpose is to answer any questions and refer to the documents via function call"
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


async def initialize_session(openai_ws, qa):
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
        }
    }

    tools = [{
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
    ]

    tool_choice = "auto"

    if qa != None:
        session_update['session']['tools'] = tools
        session_update['session']['tool_choice'] = tool_choice
    
    print('Sending session update:', json.dumps(session_update))
    await openai_ws.send(json.dumps(session_update))

    # Uncomment the next line to have the AI speak first
    await send_initial_conversation_item(openai_ws)



    # async def initialize_session(openai_ws):
    # """Control initial session with OpenAI."""
    # session_update = {
    #     "type": "session.update",
    #     "session": {
    #         "turn_detection": {"type": "server_vad"},
    #         "input_audio_format": "g711_ulaw",
    #         "output_audio_format": "g711_ulaw",
    #         "voice": VOICE,
    #         "instructions": SYSTEM_MESSAGE,
    #         "modalities": ["text", "audio"],
    #         "temperature": 0.8,
    #         "input_audio_transcription": {
    #             "model": "gpt-4o-transcribe",
    #         },
    #         "tools": [{
    #             "type": "function",
    #             "name": "query_documents",
    #             "description": "If the caller is asking about something that pertains the person they were trying to call, then this function will be called",
    #             "parameters": {
    #                 "type": "object",
    #                 "properties": {
    #                     "query": {
    #                         "type": "string",
    #                         "description": "what you need to be able to query for the semantic search of the documents",
    #                     }
    #                 },
    #                 "required": ["query"]
    #             }
    #         },
    #     ],
    #     "tool_choice": "auto",
    #     }
    # }