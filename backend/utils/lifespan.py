from contextlib import asynccontextmanager
from utils.db import get_mongo_collection
from utils.access_token import decode_access_token, create_access_token
from fastapi import FastAPI
from utils.data import get_data



@asynccontextmanager
async def lifespan(app: FastAPI):
    collection, client = get_mongo_collection(testing=True)
    app.state.collection = collection

    app.state.decode_token = decode_access_token
    app.state.create_token = create_access_token

    app.state.get_data = get_data

    




    yield
    client.close()
