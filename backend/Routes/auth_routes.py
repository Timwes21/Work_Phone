from fastapi import APIRouter, Request
from utils.db import collection
from fastapi.responses import JSONResponse
import json
from passlib.context import CryptContext
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
from utils.access_token import decode_access_token, create_access_token
from utils.data import get_data





router = APIRouter()


@router.post("/login", response_class=JSONResponse)
async def login(request: Request):
    data = await get_data(request)
    
    username, possible_password = data.values()
    possible_user = await collection.find_one({"username": username})
    
    if possible_user.keys() == 0:
        return {"logged_in": False, "message": "username does not exist"}
    
    password = possible_user["password"]
    password_match = pwd_context.verify(possible_password, password)
    
    if not password_match:
        return {"logged_in": False, "message": "password in incorrect"}
    
    # if len(possible_user["tokens"]) > 4:
    #     return {"logged_in": False, "message": "Only up to 4 devices can be logged in"}
    
    [token, current] = create_access_token()
    await collection.update_one({"username": username}, {"$push": {"tokens": current}})
    return {"logged_in": True, "message": "Logged In!", "token": token}

    

@router.post("/logout", response_class=JSONResponse)
async def logout(request: Request):
    print("**In logout**")
    data: dict = await get_data(request)
    token: str = data["token"]
    print(f"**Got token: {token}")
    await collection.update_one({"tokens": token}, {"$pull": {"tokens": token}})
    return {"message": "Logged Out"}
    

@router.post("/create-account", response_class=JSONResponse)
async def create_account(request: Request):
    print("**In create_account**")
    data: dict = await get_data(request)
    username, password, number, email = data.values()
    hashed_password = pwd_context.hash(password)
    new_number = number.replace(" ", "").replace("(", "").replace(")", "").replace("-", "")
    [token, current_time] = create_access_token()
    document = {
        "username": username,
        "password": hashed_password,
        "email": email,
        "twilio_number" : f"+1{new_number}",
        "tokens": [current_time],
        "files": []
    }
    await collection.insert_one(document)
    return {"token": token, "message": "Logged In"}



