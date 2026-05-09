from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from bson import ObjectId
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
import os

from app.database import user_collection
from app.routes.health import router as health_router
from app.routes.rag import router as rag_router

# Load environment variables
load_dotenv()

# Create Gemini model using LangChain
model = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=os.getenv("GOOGLE_API_KEY")
)

# Create FastAPI app
app = FastAPI(title="RAG API")

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
app.include_router(health_router)
app.include_router(rag_router)


# Home Route
@app.get("/")
def home():
    return {"message": "RAG API is running"}


# Create User
@app.post("/users")
def create_user(user: dict):
    result = user_collection.insert_one(user)
    return {
        "id": str(result.inserted_id),
        "message": "User created"
    }


# Get All Users
@app.get("/users")
def get_users():
    users = []

    for user in user_collection.find():
        user["_id"] = str(user["_id"])
        users.append(user)

    return users


# Get Single User
@app.get("/users/{user_id}")
def get_user(user_id: str):
    try:
        user = user_collection.find_one({"_id": ObjectId(user_id)})
    except:
        return {"message": "Invalid user ID"}

    if user is None:
        return {"message": "User not found"}

    user["_id"] = str(user["_id"])
    return user


# Update User
@app.put("/users/{user_id}")
def update_user(user_id: str, updated_user: dict):
    try:
        user_collection.update_one(
            {"_id": ObjectId(user_id)},
            {"$set": updated_user}
        )
    except:
        return {"message": "Invalid user ID"}

    return {"message": "User updated"}


# Delete User
@app.delete("/users/{user_id}")
def delete_user(user_id: str):
    try:
        user_collection.delete_one({"_id": ObjectId(user_id)})
    except:
        return {"message": "Invalid user ID"}

    return {"message": "User deleted"}


# Gemini Chat Endpoint
@app.post("/chat")
def chat(question: str):
    response = model.invoke(question)
    return {"answer": response.content}