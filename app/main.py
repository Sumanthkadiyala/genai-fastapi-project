from fastapi import FastAPI
from app.database import user_collection
from bson import ObjectId

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Hello World"}

@app.get("/health")
def health():
    return {"status": "healthy"}

@app.post("/users")
def create_user(user: dict):

    result = user_collection.insert_one(user)

    return {
        "id": str(result.inserted_id),
        "message": "User created"
    }

@app.get("/users")
def get_users():

    users = []

    for user in user_collection.find():

        user["_id"] = str(user["_id"])

        users.append(user)

    return users

@app.get("/users/{user_id}")
def get_user(user_id: str):

    user = user_collection.find_one(
        {"_id": ObjectId(user_id)}
    )

    user["_id"] = str(user["_id"])

    return user

@app.put("/users/{user_id}")
def update_user(user_id: str, updated_user: dict):

    user_collection.update_one(
        {"_id": ObjectId(user_id)},
        {"$set": updated_user}
    )

    return {
        "message": "User updated"
    }

@app.delete("/users/{user_id}")
def delete_user(user_id: str):

    user_collection.delete_one(
        {"_id": ObjectId(user_id)}
    )

    return {
        "message": "User deleted"
    }

from google import genai
from fastapi import FastAPI
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI()

client = genai.Client(
    api_key=os.getenv("GOOGLE_API_KEY")
)

@app.post("/chat")
def chat(question: str):

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=question
    )

    return {
        "answer": response.text
    }

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)