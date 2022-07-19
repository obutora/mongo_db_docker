import json
from datetime import datetime
import os
from fastapi import FastAPI
from pymongo import MongoClient
from pydantic import BaseModel
from typing import Optional, List

from bson.objectid import ObjectId
from bson.json_util import dumps, loads

from dotenv import load_dotenv
load_dotenv()


host = 'mongo'
port = 27017
user = os.getenv('MONGO_USER')
password = os.getenv('MONGO_PASS')

client = MongoClient(host=host, port=port, username=user, password=password)
db = client['drugHistory']
collection = db['history']

app = FastAPI()


class Soap(BaseModel):
    id: str
    soap: str
    body: str


class History(BaseModel):
    id: str
    group: List[str]
    date: str
    hotString: str
    soapList: List[Soap]


@app.get("/")
async def read_root():
    result = collection.find()
    print(dumps(result))
    # return {"helo": "World"}
    return dumps(result)


@app.post("/add")
async def add_history(history: History):
    # collection.insert_one(testJson)
    # j = json.dumps(history.dict())  # NOTE: dict にしないと、json.dumps でエラーが出る
    # print(j)

    try:
        collection.insert_one(history.dict())
        return {'status': 'ok'}
    except Exception as e:
        print(e)
        return {'status': 'error'}
