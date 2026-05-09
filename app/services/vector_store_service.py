import os
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS

from app.services.document_loader import load_documents
from app.services.embeddings_service import get_embeddings
from app.config.settings import settings


def create_vector_store():
    documents = load_documents()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )

    chunks = splitter.split_documents(documents)

    embeddings = get_embeddings()

    vector_store = FAISS.from_documents(
        documents=chunks,
        embedding=embeddings
    )

    os.makedirs(settings.VECTOR_STORE_PATH, exist_ok=True)

    vector_store.save_local(settings.VECTOR_STORE_PATH)

    return {
        "documents_loaded": len(documents),
        "chunks_created": len(chunks)
    }


def load_vector_store():
    embeddings = get_embeddings()

    return FAISS.load_local(
        settings.VECTOR_STORE_PATH,
        embeddings,
        allow_dangerous_deserialization=True
    )