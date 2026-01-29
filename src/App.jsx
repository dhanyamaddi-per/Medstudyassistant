import { useMemo, useState } from "react";
import axios from "axios";
import "./index.css";

const API_BASE = "http://127.0.0.1:8000";

export default function App() {
  const [mode, setMode] = useState("explain");
  const [difficulty, setDifficulty] = useState("medium");
  const [model, setModel] = useState("llama3.1:8b");

  const [question, setQuestion] = useState("");
  const [userAnswer, setUserAnswer] = useState("");
  const [messages, setMessages] = useState([]);
  const [citations, setCitations] = useState([]);
  const [uploadStatus, setUploadStatus] = useState("");

  /* ==========================
     FILE UPLOAD
     ========================== */
  async function uploadPdf(file) {
    const formData = new FormData();
    formData.append("file", file);

    const res = await fetch(`${API_BASE}/upload`, {
      method: "POST",
      body: formData,
    });

    if (!res.ok) {
      const text = await res.text();
      throw new Error(text);
    }

    return await res.json(); // { status, filename }
  }

  async function uploadFile(e) {
    const file = e.target.files?.[0];
    if (!file) return;

    setUploadStatus("Uploading PDF...");
    try {
      const data = await uploadPdf(file);
      setUploadStatus(`Uploaded: ${data.filename}`);
    } catch (err) {
      console.error(err);
      setUploadStatus(`Upload failed: ${err.message}`);
    }
  }

  /* ==========================
     INGEST
     ========================== */
  async function ingest() {
    setUploadStatus("Indexing (ingest)...");
    try {
      const res = await axios.post(`${API_BASE}/ingest`);
      setUploadStatus(
        `Ingest complete → PDFs: ${res.data.pdf_count}, Pages: ${res.data.pages_loaded}`
      );
    } catch (err) {
      console.error(err);
      setUploadStatus(
        `Ingest failed: ${err?.response?.data || err.message}`
      );
    }
  }

  /* ==========================
     CHAT
     ========================== */
  async function send() {
    const q = question.trim();
    if (!q) return;

    setMessages((m) => [...m, { role: "user", text: q }]);
    setQuestion("");

    try {
      const payload = {
        question: q,
        mode,
        difficulty,
        user_answer: mode === "grade" ? userAnswer : "",
        model,
      };

      const res = await axios.post(`${API_BASE}/chat`, payload);

      setMessages((m) => [
        ...m,
        { role: "assistant", text: res.data.answer },
      ]);
      setCitations(res.data.citations || []);
    } catch (err) {
      console.error(err);
      setMessages((m) => [
        ...m,
        {
          role: "assistant",
          text: "Request failed. Is the backend running?",
        },
      ]);
    }
  }

  const showGradeBox = useMemo(() => mode === "grade", [mode]);

  /* ==========================
     UI
     ========================== */
  return (
    <div className="app">
      <header className="header">
        <div>
          <h1>Med Study Assistant</h1>
          <p className="sub">
            RAG (Chroma) + CrewAI Agents + Local LLM (Ollama)
          </p>
        </div>
      </header>

      <div className="layout">
        {/* LEFT PANEL */}
        <aside className="panel">
          <h2>Documents</h2>

          <input
            type="file"
            accept="application/pdf"
            onChange={uploadFile}
          />

          <button onClick={ingest}>Ingest PDFs</button>

          <div className="status">{uploadStatus}</div>

          <h2>Study Mode</h2>
          <select value={mode} onChange={(e) => setMode(e.target.value)}>
            <option value="explain">Explain</option>
            <option value="quiz">Quiz</option>
            <option value="flashcards">Flashcards</option>
            <option value="grade">Grade</option>
          </select>

          <h2>Quiz Difficulty</h2>
          <select
            value={difficulty}
            onChange={(e) => setDifficulty(e.target.value)}
          >
            <option value="easy">easy</option>
            <option value="medium">medium</option>
            <option value="hard">hard</option>
          </select>

          <h2>Model</h2>
          <input
            value={model}
            onChange={(e) => setModel(e.target.value)}
            placeholder="llama3.1:8b"
          />
          <p className="hint">Example: llama3.1:8b or gemma2:2b</p>

          <h2>Citations</h2>
          <div className="citations">
            {citations.length === 0 ? (
              <div className="muted">No citations yet.</div>
            ) : (
              citations.map((c, i) => (
                <div key={i} className="cite">
                  <div className="citeTitle">
                    {c.source} — p.{c.page}
                  </div>
                  <div className="citeSnippet">{c.snippet}</div>
                </div>
              ))
            )}
          </div>
        </aside>

        {/* CHAT */}
        <main className="chat">
          <div className="messages">
            {messages.map((m, i) => (
              <div key={i} className={`msg ${m.role}`}>
                <div className="bubble">
                  <div className="role">
                    {m.role === "user" ? "You" : "Assistant"}
                  </div>
                  <pre className="text">{m.text}</pre>
                </div>
              </div>
            ))}
          </div>

          <div className="composer">
            <textarea
              value={question}
              onChange={(e) => setQuestion(e.target.value)}
              placeholder="Ask: Explain cardiac action potential from my notes…"
              rows={3}
            />

            {showGradeBox && (
              <textarea
                value={userAnswer}
                onChange={(e) => setUserAnswer(e.target.value)}
                placeholder="(Grade mode) Paste your answer here…"
                rows={3}
              />
            )}

            <button onClick={send}>Send</button>
          </div>
        </main>
      </div>
    </div>
  );
}
