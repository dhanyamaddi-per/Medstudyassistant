import os
from typing import List
from pypdf import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from .vectordb import get_vectordb

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
UPLOAD_DIR = os.path.join(BASE_DIR, "storage", "uploads")

def load_pdf_as_documents(pdf_path: str) -> List[Document]:
    reader = PdfReader(pdf_path)
    docs = []
    for page_idx, page in enumerate(reader.pages):
        text = page.extract_text() or ""
        text = text.strip()
        if not text:
            continue
        docs.append(
            Document(
                page_content=text,
                metadata={
                    "source": os.path.basename(pdf_path),
                    "page": page_idx + 1
                },
            )
        )
    return docs

def ingest_all_pdfs() -> dict:
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    vectordb = get_vectordb()

    pdfs = [f for f in os.listdir(UPLOAD_DIR) if f.lower().endswith(".pdf")]
    if not pdfs:
        return {"status": "no_files", "message": "No PDFs found in uploads folder."}

    splitter = RecursiveCharacterTextSplitter(chunk_size=900, chunk_overlap=150)

    total_docs = 0
    total_chunks = 0

    for pdf in pdfs:
        path = os.path.join(UPLOAD_DIR, pdf)
        docs = load_pdf_as_documents(path)
        total_docs += len(docs)

        chunks = splitter.split_documents(docs)
        total_chunks += len(chunks)

        vectordb.add_documents(chunks)

    
    return {
        "status": "ok",
        "pdf_count": len(pdfs),
        "pages_loaded": total_docs,
        "chunks_added": total_chunks,
    }
