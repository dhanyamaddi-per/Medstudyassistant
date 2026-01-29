import os
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma


BASE_DIR = os.path.dirname(os.path.dirname(__file__))
CHROMA_DIR = os.path.join(BASE_DIR, "storage", "chroma_db")

# Medical-friendly embedding model (works well with med terms)
EMBED_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

def get_embeddings():
    return HuggingFaceEmbeddings(model_name=EMBED_MODEL)

def get_vectordb():
    embeddings = get_embeddings()
    os.makedirs(CHROMA_DIR, exist_ok=True)
    return Chroma(persist_directory=CHROMA_DIR, embedding_function=embeddings)
