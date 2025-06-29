import json
from utils.access_token import decode_access_token

async def get_data(request) -> dict:
    data = await request.body()
    data = data.decode()
    data = json.loads(data)
    if "token" in data:
        data["token"] = decode_access_token(data["token"])
    return data
