from twilio.twiml.voice_response import VoiceResponse, Connect, Say, Stream
from fastapi.responses import HTMLResponse

def dial_person():
    my_number = "+17726210972"
    response = VoiceResponse()
    dial = response.dial(number=my_number,action="/get-call-status", timeout=5)
    response = VoiceResponse()
    response.append(dial)
    return HTMLResponse(content=str(response), media_type="application/xml")

def dial_agent(request):
    my_name = "Tim"
    response = VoiceResponse()
    # <Say> punctuation to improve text-to-speech flow
    response.say(f"You are being connected to {my_name}'s AI Assistant")
    response.pause(length=1)
    response.say("Say Hi to start conversation")
    host = request.url.hostname
    connect = Connect()
    connect.stream(url=f'wss://{host}/media-stream')
    response.append(connect)
    return HTMLResponse(content=str(response), media_type="application/xml")