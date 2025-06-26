from fastapi import APIRouter, Request
from utils.db import collection
from passlib.context import CryptContext
from jwt import encode, decode
from fastapi.responses import JSONResponse
import time
import os
from dotenv import load_dotenv
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

load_dotenv()

SECRET_KEY = os.environ["SECRET_KEY"]
ALGORITHM = os.environ["ALGORITHM"]

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def create_access_token():
    current = time.time()
    encoded_jwt = encode(current, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt



router = APIRouter()


# Create an instance of CryptContext to manage the hashing and verification
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@router.post("/login", response_class=JSONResponse)
async def login(request: Request):
    data = await request.body()
    username, possible_password = data.values()
    possible_user = collection.find_one({"username": username})
    if possible_user.keys() == 0:
        return {"logged_in": False, "message": "username does not exist"}
    password = possible_user["password"]
    password_match = pwd_context.verify(password, possible_password)
    if not password_match:
        return {"logged_in": False, "message": "password in incorrect"}
    if len(possible_user["files"]) > 4:
        return {"logged_in": False, "message": "Only up to 4 devices can be logged in"}
    token = create_access_token()
    collection.update_one({"username": username}, {"$push": {"tokens": token}})
    return {"logged_in": True, "message": "Logged In!", "token": token}

    

@router.post("/logout", response_class=JSONResponse)
async def logout(request: Request):
    data = await request.body()
    token = data["token"]
    collection.update_one({"tokens": token}, {"$pop": {"tokens": token}})
    return {"message": "Logged Out"}
    

@router.post("/create-account", response_class=JSONResponse)
async def create_account(request: Request):
    data = await request.body()
    
    username, password, number = data.values()
    hashed_password = pwd_context.hash(password)
    
    token = create_access_token()
    document = {
        "username": username,
        "password": hashed_password,
        "number" : f"+1{number}",
        "tokens": [token]
        
    }
    collection.insert_one(document)    
    return {"token": token}



