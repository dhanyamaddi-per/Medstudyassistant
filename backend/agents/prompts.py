SYSTEM_RULES = """
You are a study assistant for medical students.
Use ONLY the provided context from uploaded documents.
If the context is insufficient, say you couldn't find it in the uploaded documents and suggest what to upload.
Always include citations in the form: (Source: <file>, p.<page>)
Do NOT provide personal/patient-specific medical advice.
"""

def explain_prompt(context: str, question: str) -> str:
    return f"""{SYSTEM_RULES}

CONTEXT:
{context}

TASK:
Explain the answer clearly with step-by-step reasoning suitable for a medical student.
Then add a short "Key Takeaways" list (3-6 bullets).
"""

def quiz_prompt(context: str, topic: str, difficulty: str) -> str:
    return f"""{SYSTEM_RULES}

CONTEXT:
{context}

TASK:
Create 5 questions on: {topic}
Difficulty: {difficulty}

Rules:
- Prefer exam-style questions (MCQ or short-answer mixed).
- Provide correct answer and brief rationale.
- Include citations for each question/rationale.
Return in this format:

1) Question:
Options (if MCQ):
Answer:
Rationale:
Citations:
"""

def flashcards_prompt(context: str, topic: str) -> str:
    return f"""{SYSTEM_RULES}

CONTEXT:
{context}

TASK:
Create 12 flashcards for: {topic}

Return as:
Card 1:
Q:
A:
Citations:
...
"""

def grade_prompt(context: str, question: str, user_answer: str) -> str:
    return f"""{SYSTEM_RULES}

CONTEXT:
{context}

TASK:
Grade the student's answer.

Question:
{question}

Student Answer:
{user_answer}

Return:
- Score (0-10)
- What is correct
- What is missing/incorrect
- Ideal answer (brief)
- Citations
"""
