import os
from pymongo import AsyncMongoClient
from dotenv import load_dotenv

load_dotenv()

mongodb_uri = os.getenv("MONGODB_URI")
mongodb_db = os.getenv("MONGODB_DB")

client = AsyncMongoClient(mongodb_uri)
db = client[mongodb_db]
todos_collection = db["todos"]

def get_database():
     return db

async def check_connection():
    try:
        await client.admin.command("ping")
        return True
    except Exception as e:
        print(f"Error checking connection: {e}")
        return False
