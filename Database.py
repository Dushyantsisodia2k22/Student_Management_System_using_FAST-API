from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import os

load_dotenv()

Mongo_URI = os.getenv("connection_string")

client = AsyncIOMotorClient(Mongo_URI)

db = client["Student_Database"]
students_collection = db['Student_Collections']

