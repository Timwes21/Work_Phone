from twilio.twiml.voice_response import VoiceResponse, Connect, Say, Stream
from fastapi.responses import HTMLResponse
from utils.db import collection

async def dial_person(twilio_number):
    res = await collection.find_one({"twilio_number": twilio_number})
    personal_number = res["real_number"]
    print(personal_number)
    my_number = f"+1{personal_number}"
    response = VoiceResponse()
    dial = response.dial(number=my_number, action=f"/ai-assistant/get-call-status/{twilio_number}", timeout=15)
    response = VoiceResponse()
    response.append(dial)
    return HTMLResponse(content=str(response), media_type="application/xml")

async def dial_agent(request, number, route):
    res = await collection.find_one({"twilio_number": number})
    name = res["name"]
    response = VoiceResponse()
    response.say(f"You are being connected to {name}'s AI Assistant")
    host = request.url.hostname
    connect = Connect()
    url=f'wss://{host}/{route}/media-stream/{number}'
    print(url)
    connect.stream(url=url)
    response.append(connect)
    print("int dial agent")
    return HTMLResponse(content=str(response), media_type="application/xml")

