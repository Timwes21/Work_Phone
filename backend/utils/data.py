import json
from fastapi import Request
from utils.access_token import decode_access_token

async def get_data(request: Request) -> dict:
    data = await request.body()
    data = data.decode()
    data = json.loads(data)
    if "token" in request.headers:
        data["token"] = decode_access_token(request.headers["token"])
    return data
