from pymongo import AsyncMongoClient
from motor.motor_asyncio import AsyncIOMotorClient
import pymongo
from dotenv import load_dotenv
import os
load_dotenv()


def get_mongo_collection(testing):
    url = os.environ["MONGO_URL"]
    collection_name = "test" if testing else "production"
    url = os.environ["MONGO_URL"]
    client = AsyncIOMotorClient(url)
    db = client["work-phone"]
    return db[collection_name], client



