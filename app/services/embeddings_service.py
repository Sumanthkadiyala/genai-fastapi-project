from langchain_community.embeddings import HuggingFaceEmbeddings
from app.config.settings import settings


def get_embeddings():
    return HuggingFaceEmbeddings(
        model_name=settings.EMBEDDING_MODEL
    )