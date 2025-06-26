from pymongo import MongoClient
from dotenv import load_dotenv
import os
load_dotenv()

testing = True
collection_name = "test" if testing else "production"

url = os.environ["MONGO_URL"]
work_number = os.environ["NUMBER"]
client = MongoClient(url)
db = client["work-phone"]
collection = db[collection_name]


def add_call_log(log):
    collection.update_one({"number": work_number}, {"$push": {"logs": log}})

def missed_call_logs():
    results = collection.find_one({"number": work_number}, {"_id": 0})
    return results["logs"]


