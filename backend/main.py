from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pymongo import MongoClient
import os
from dotenv import load_dotenv
from model_selector import generate_session_id

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

mongo_url = os.getenv("MONGO_URL")
client = MongoClient(mongo_url)
db = client["chatbot"]
collection = db["sessions"]

@app.get("/")
def root():
    return {"message": "Chatbot backend is running"}

@app.get("/menu")
def get_menu():
    """Return available models as selection choices."""
    return {"models": ["main1", "main2"]}

@app.post("/start")
async def start_session(request: Request):
    """Start a new chat session with chosen model."""
    data = await request.json()
    model = data.get("model")
    if model not in ["main1", "main2"]:
        return {"error": "Invalid model choice"}
    session_id = generate_session_id()
    collection.insert_one({
        "session_id": session_id,
        "model": model,
        "messages": []
    })
    return {"session_id": session_id, "model": model}
