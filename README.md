# 🩺 MedStudyAssistant – Medical Study Chatbot (RAG + Agents + Local LLM)

MedStudyAssistant is a **teaching and study assistant chatbot for medical students**, built using **Retrieval-Augmented Generation (RAG)**, **CrewAI agents**, **Chroma vector database**, and a **fully local LLM using Ollama**.

The system answers questions **strictly from uploaded medical PDFs**, providing **accurate citations (source + page number)**.  
It runs **completely locally**, with **no paid APIs and no OpenAI key required**.

---

## 🔁 How the System Works (Workflow)

1. User uploads medical PDFs (textbooks, notes, manuals)
2. PDFs are ingested:
   - Text extraction
   - Chunking
   - Embedding generation
   - Storage in Chroma vector database
3. User asks a question from the frontend
4. Backend retrieves relevant chunks (RAG)
5. CrewAI agent reasons over retrieved context
6. Local LLM (Ollama) generates the answer
7. Answer is returned with citations

---

## ✨ Features

- Upload medical PDFs
- RAG-based question answering
- Persistent Chroma vector database
- CrewAI agent-based reasoning
- Local LLM via Ollama (LLaMA / Gemma)
- Study modes:
  - Explain
  - Quiz
  - Flashcards
  - Grade answers
- React frontend + FastAPI backend
- Citation-backed responses

---

## ⚙️ Prerequisites

Install the following before starting:

- **Python 3.10.x**
- **Node.js (LTS)**
- **Ollama**instaLled locally

---

## ✅ STEP 1: Install and Run Ollama (Local LLM)

1. Download and install Ollama:
   https://ollama.com

2. Pull a local model:
   ```bash
   ollama pull llama3.1:8b
 

---

## Step 2 – Backend Setup (FastAPI)

Create and activate a Python virtual environment and install dependencies:

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt


## Step 3 – Start the Backend Server

From the project root directory, start the FastAPI server:

uvicorn backend.main:app --reload --port 8000

The backend will run at:

http://127.0.0.1:8000

API documentation will be available at:

http://127.0.0.1:8000/docs

---

## Step 4 – Add Medical PDFs

Place all medical PDFs (textbooks, notes, manuals) into the following directory:

backend/data/pdfs/

Example:

backend/data/pdfs/Applied_Human_Anatomy.pdf

These documents act as the knowledge source for the chatbot.

---

## Step 5 – Ingest / Index PDFs

Run the ingestion process to build the vector database:

python -c "from backend.rag.ingest import ingest_all_pdfs; print(ingest_all_pdfs())"

Example output:

{
  "status": "ok",
  "pdf_count": 1,
  "pages_loaded": 167,
  "chunks_added": 268
}

Indexing may take time for large medical textbooks. This is expected because the process involves PDF parsing, chunking, and embedding generation.

---

## Step 6 – Frontend Setup and Run (React)

Open a new terminal window, then run:

cd frontend  
npm install  
npm run dev  

The frontend will run at:

http://localhost:5173

---

## Using the Application

Open the frontend in your browser

Upload a medical PDF

Click “Ingest PDFs”

Select a study mode (Explain, Quiz, Flashcards, Grade)

Ask questions based on the uploaded notes

Receive answers with citations

---

## Study Modes

Explain – Explains medical concepts grounded in the uploaded notes  

Quiz – Generates exam-style questions with answers  

Flashcards – Creates concise question-answer cards  

Grade – Grades a student’s answer using the notes  

---

## Notes

Chroma vector database persists automatically  

No manual save is required  

Indexed data remains across restarts  

The system uses a local LLM via Ollama and does not rely on OpenAI




























