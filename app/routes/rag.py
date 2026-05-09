from fastapi import APIRouter
from app.models.chat_models import QuestionRequest
from app.services.vector_store_service import create_vector_store
from app.services.rag_service import ask_rag

router = APIRouter(prefix="/rag", tags=["RAG"])


@router.get("/build-index")
def build_index():
    result = create_vector_store()
    return {
        "message": "FAISS index created successfully",
        "details": result
    }


@router.post("/chat")
def rag_chat(request: QuestionRequest):
    answer = ask_rag(request.question)
    return {
        "response": answer
    }