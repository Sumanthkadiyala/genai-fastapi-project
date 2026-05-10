from fastapi import APIRouter
from app.models.chat_models import QuestionRequest
from app.services.agent_service import ask_agent

router = APIRouter(
    prefix="/agent",
    tags=["AI Agent"]
)


@router.post("/chat")
def agent_chat(request: QuestionRequest):
    response = ask_agent(request.question)

    return {
        "response": response
    }