from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from passlib.context import CryptContext
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")





router = APIRouter()


@router.post("/login", response_class=JSONResponse)
async def login(request: Request):
    data = await request.app.state.get_data(request)
    collection = request.app.state.collection
    
    username, possible_password = data.values()
    possible_user = await collection.find_one({"username": username}) or None
    
    if not possible_user:
        return {"logged_in": False, "message": "username does not exist"}
    
    password = possible_user["password"]
    password_match = pwd_context.verify(possible_password, password)
    
    if not password_match:
        return {"logged_in": False, "message": "password in incorrect"}
    
    
    [token, current] = request.app.state.create_token()
    await collection.update_one({"username": username}, {"$push": {"tokens": current}})
    return {"logged_in": True, "message": "Logged In!", "token": token}

    

@router.post("/logout", response_class=JSONResponse)
async def logout(request: Request):
    print("**In logout**")
    collection = request.app.state.collection
    data: dict = await request.app.state.get_data(request)
    token: str = data["token"]
    await collection.update_one({"tokens": token}, {"$pull": {"tokens": token}})
    return {"message": "Logged Out"}
    

@router.post("/create-account", response_class=JSONResponse)
async def create_account(request: Request):
    print("**In create_account**")
    collection = request.app.state.collection
    data: dict = await request.app.state.get_data(request)
    username, password, name, twilio_number, real_number = data.values()
    possible_account = collection.find_one({"username": username})
    if not possible_account:
        return {"message": "Username Already Exists"}
    [token, current_time] = request.app.state.create_access_token()
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


@router.get("/user-settings", response_class=JSONResponse)
async def user_settings(request: Request):
    token = request.headers['token']
    token = request.app.state.decode_token(token)
    collection = request.app.state.collection
    result = await collection.find_one({'tokens': token}, {"name":1, "real_number": 1, "twilio_number":1, "_id":0})
    return result

@router.post("/change-user-settings", response_class=JSONResponse)
async def change_user_settings(request: Request):
    data: dict = await request.app.state.get_data(request)
    changed = data["changed"]
    print(changed)
    collection =request.app.state.collection
    await collection.update_one({"tokens": data['token']}, {"$set": changed})
    return {"Changed": "Success"}



