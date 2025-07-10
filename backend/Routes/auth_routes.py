from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from passlib.context import CryptContext
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
from utils.access_token import decode_access_token, create_access_token
from utils.data import get_data





router = APIRouter()


@router.post("/login", response_class=JSONResponse)
async def login(request: Request):
    data = await get_data(request)
    collection = request.app.state.collection
    
    username, possible_password = data.values()
    possible_user = await collection.find_one({"username": username}) or None
    
    if not possible_user:
        return {"logged_in": False, "message": "username does not exist"}
    
    password = possible_user["password"]
    password_match = pwd_context.verify(possible_password, password)
    
    if not password_match:
        return {"logged_in": False, "message": "password in incorrect"}
    
    
    [token, current] = create_access_token()
    await collection.update_one({"username": username}, {"$push": {"tokens": current}})
    return {"logged_in": True, "message": "Logged In!", "token": token}

    

@router.post("/logout", response_class=JSONResponse)
async def logout(request: Request):
    print("**In logout**")
    collection = request.app.state.collection
    data: dict = await get_data(request)
    token: str = data["token"]
    await collection.update_one({"tokens": token}, {"$pull": {"tokens": token}})
    return {"message": "Logged Out"}
    

@router.post("/create-account", response_class=JSONResponse)
async def create_account(request: Request):
    print("**In create_account**")
    collection = request.app.state.collection
    data: dict = await get_data(request)
    username, password, name, twilio_number, real_number = data.values()
    [token, current_time] = create_access_token()
    document = {
        "username": username,
        "password": pwd_context.hash(password),
        "name": name,
        "twilio_number" : twilio_number.replace(" ", "").replace("(", "").replace(")", "").replace("-", ""),
        "real_number": real_number,
        "tokens": [current_time],
        "files": []
    }
    await collection.insert_one(document)
    return {"token": token, "message": "Logged In"}




