import os
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from backend.rag.ingest import ingest_all_pdfs
from backend.rag.retrieve import retrieve_with_citations
from backend.agents.safety import safety_check_study_only, STUDY_ONLY_MESSAGE
from backend.agents.crew import route_mode, run_explain, run_quiz, run_flashcards, run_grade

BASE_DIR = os.path.dirname(__file__)
UPLOAD_DIR = os.path.join(BASE_DIR, "storage", "uploads")

app = FastAPI(title="Med Study Assistant (RAG + CrewAI)")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ChatRequest(BaseModel):
    question: str
    mode: str = "explain"          # explain | quiz | flashcards | grade
    difficulty: str = "medium"     # used for quiz
    user_answer: str = ""          # used for grade
    model: str = "llama3.1:8b"     # change to gemma2:2b if needed

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/")
def root():
    return {"message": "Backend is running. Go to /docs"}


@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    if not file.filename.lower().endswith(".pdf"):
        return {"status": "error", "message": "Only PDF files are supported."}

    save_path = os.path.join(UPLOAD_DIR, file.filename)
    content = await file.read()
    with open(save_path, "wb") as f:
        f.write(content)

    return {"status": "ok", "filename": file.filename}

@app.post("/ingest")
def ingest():
    return ingest_all_pdfs()

@app.post("/chat")
def chat(req: ChatRequest):
    if not safety_check_study_only(req.question):
        return {"answer": STUDY_ONLY_MESSAGE, "citations": [], "mode": "blocked"}

    mode = route_mode(req.mode)

    # Retrieve RAG context for all modes
    retrieved = retrieve_with_citations(
        query=req.question if mode != "quiz" else req.question,
        k=7
    )
    context = retrieved["context"]
    citations = retrieved["citations"]

    if not context.strip():
        return {
            "answer": "I couldn’t find relevant content in your uploaded PDFs. Upload notes for this topic, then click Ingest.",
            "citations": [],
            "mode": mode
        }

    if mode == "explain":
        answer = run_explain(context=context, question=req.question, model_name=req.model)
    elif mode == "quiz":
        answer = run_quiz(context=context, topic=req.question, difficulty=req.difficulty, model_name=req.model)
    elif mode == "flashcards":
        answer = run_flashcards(context=context, topic=req.question, model_name=req.model)
    elif mode == "grade":
        if not req.user_answer.strip():
            return {"answer": "Provide user_answer to grade.", "citations": citations, "mode": mode}
        answer = run_grade(context=context, question=req.question, user_answer=req.user_answer, model_name=req.model)
    else:
        answer = run_explain(context=context, question=req.question, model_name=req.model)

    return {"answer": answer, "citations": citations, "mode": mode}
