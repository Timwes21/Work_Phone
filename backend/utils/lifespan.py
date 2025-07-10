from contextlib import asynccontextmanager
from utils.db import get_mongo_collection
from fastapi import FastAPI



@asynccontextmanager
async def lifespan(app: FastAPI):
    collection, client = get_mongo_collection(testing=True)
    app.state.collection = collection


    yield
    client.close()
