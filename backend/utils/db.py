from pymongo import MongoClient
from pymongo import AsyncMongoClient
from dotenv import load_dotenv
import os
load_dotenv()

testing = True
collection_name = "test" if testing else "production"

url = os.environ["MONGO_URL"]
work_number = os.environ["NUMBER"]
client = AsyncMongoClient(url)

db = client["work-phone"]
collection = db[collection_name]


