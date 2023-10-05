import os
import time
import binascii
from typing import Dict
import jwt
from decouple import config
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pymongo.mongo_client import MongoClient
from app import return_response,return_first_response
import uvicorn


# Loading ENV variables
load_dotenv()
DB_ACCESS = os.getenv('DB_ACCESS')

# Authentication
JWT_SECRET = config("secret")
JWT_ALGORITHM = config("algorithm")

def decodeJWT(token: str) -> dict:
    try:
        decoded_token = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return decoded_token #if decoded_token["expires"] >= time.time() else None
    except:
        return {}
    

# Initializing FastAPI
app = FastAPI()

# MongoDB Connection :
def dbConnection():
    try:
        client = MongoClient(DB_ACCESS)
        db = client.get_database("Test")
        return db.get_collection("PR_Chat")
    except Exception as e:
        return Exception("Connection Failed")


@app.get("/chat")
async def chat_with_bot(token:dict):
    token_str = token['access_token']
    data = decodeJWT(token_str)
    try:
        user_id = data["user_id"]
        input_text = data["prompt"]
        db = dbConnection()
        print(db)
        user = db.find_one({"user_id":user_id})
        if user == None: 
            response = return_first_response(input_text)
            db.insert_one({"user_id":user_id,"qna":[[input_text,response]]})
            return response
        
        elif user != None:
            QnA = user["qna"]
            response = return_response(input_text,QnA)
            QnA.append([input_text,response])
            db.find_one_and_update({"user_id":user_id} , {"$set":{"qna":QnA}})
            return response


    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/chat_del")
async def del_user(token:dict):
    # token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
    token_str = token['access_token']
    data = decodeJWT(token_str)
    try:
        user_id = data["user_id"]
        db = dbConnection()
        user = db.find_one({"user_id":user_id})
        if user != None:
            db.delete_one({"user_id":user_id})
        return {"response":"user Deleted"}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.get("/")
async def test():
	return "hello g"

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)