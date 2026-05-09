from dotenv import load_dotenv
import os

load_dotenv()

class Settings:
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
    DOCUMENTS_PATH = "documents"
    VECTOR_STORE_PATH = "vector_store/faiss_index"
    EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
    LLM_MODEL = "gemini-2.5-flash"

settings = Settings()