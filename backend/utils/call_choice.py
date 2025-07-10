from twilio.twiml.voice_response import VoiceResponse, Connect, Say, Stream
from fastapi.responses import HTMLResponse

async def dial_person(twilio_number, user):
    personal_number = user["real_number"]
    my_number = f"+1{personal_number}"
    response = VoiceResponse()
    dial = response.dial(number=my_number, action=f"/ai-assistant/get-call-status/{twilio_number}", timeout=15)
    response = VoiceResponse()
    response.append(dial)
    return HTMLResponse(content=str(response), media_type="application/xml")

async def dial_agent(request, twilio_number, route):
    collection = request.app.state.collection
    user = await collection.find_one({"twilio_number": twilio_number})
    name = user["name"]
    response = VoiceResponse()
    response.say(f"You are being connected to {name}'s AI Assistant")
    host = request.url.hostname
    connect = Connect()
    url=f'wss://{host}/{route}/media-stream/{twilio_number}'
    print(url)
    connect.stream(url=url)
    response.append(connect)
    print("int dial agent")
    return HTMLResponse(content=str(response), media_type="application/xml")

