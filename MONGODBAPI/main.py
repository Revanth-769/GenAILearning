from fastapi import FastAPI,HTTPException
from pydantic import BaseModel
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")

client = AsyncIOMotorClient(MONGO_URI)

db = client["euron_db"]
euron_data = db["euron"]

app = FastAPI()

class eurondata(BaseModel):
    name: str
    phone: int
    city: str
    course : str

@app.post("/euron/insert")
# async and await : they have to beused simultaniously.
# async is a non blocking function if this function trying to execute itself, 
# it will not block some other processes because maybe it is waiting in a queue or may be it is waiting for our database to store data 
# asnd give a response back, non blocking function is a function that will allow other inserts requests to take place here in this function
# this is must for high traffic API so that it will not be blocked motor is a driver which will provide this feature.


async def  euron_data_insert_helper(data : eurondata):
    result = await euron_data.insert_one(data.dict()) 
    return str(result.inserted_id)

def euron_helper(doc):
    doc["id"] = str(doc["_id"])
    del doc["_id"]
    return doc


@app.get("/euron/getdata")
async def get_euron_data():
    itms = []
    cursor = euron_data.find({})
    async for document in cursor:
        itms.append(euron_helper(document))

    return itms