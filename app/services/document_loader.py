from langchain_community.document_loaders import PyPDFDirectoryLoader
from app.config.settings import settings


def load_documents():
    loader = PyPDFDirectoryLoader(settings.DOCUMENTS_PATH)
    return loader.load()