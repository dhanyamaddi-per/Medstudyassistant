from crewai import Agent, Task, Crew, LLM
from .prompts import explain_prompt, quiz_prompt, flashcards_prompt, grade_prompt

def get_llm(model_name: str):
    name = (model_name or "").strip() or "llama3.1:8b"
    return LLM(
        model=f"ollama/{name}",
        base_url="http://localhost:11434"
    )

def run_explain(context: str, question: str, model_name: str) -> str:
    llm = get_llm(model_name)

    agent = Agent(
        role="Medical Explainer",
        goal="Explain medical concepts clearly using only provided context and citations.",
        backstory="You are a medical educator who grounds answers in the supplied study notes.",
        llm=llm,
        allow_delegation=False,
    )

    task = Task(
        description=explain_prompt(context, question),
        expected_output="A clear explanation grounded ONLY in the provided context, with citations when available.",
        agent=agent
    )

    crew = Crew(agents=[agent], tasks=[task])
    return str(crew.kickoff())


def run_quiz(context: str, topic: str, difficulty: str, model_name: str) -> str:
    llm = get_llm(model_name)

    agent = Agent(
        role="Quiz Generator",
        goal="Generate medical questions with answers and citations using only provided context.",
        backstory="You create exam-style questions from the given notes and cite sources.",
        llm=llm,
        allow_delegation=False,
    )

    task = Task(
        description=quiz_prompt(context, topic, difficulty),
        expected_output="5-10 quiz questions with answers, each grounded in the provided context, include citations when available.",
        agent=agent
    )

    crew = Crew(agents=[agent], tasks=[task])
    return str(crew.kickoff())


def run_flashcards(context: str, topic: str, model_name: str) -> str:
    llm = get_llm(model_name)

    agent = Agent(
        role="Flashcard Maker",
        goal="Create concise Q/A flashcards from notes with citations.",
        backstory="You help students memorize high-yield facts grounded in the notes.",
        llm=llm,
        allow_delegation=False,
    )

    task = Task(
        description=flashcards_prompt(context, topic),
        expected_output="10-20 flashcards (Q/A). Keep them concise and grounded in the provided context, include citations when available.",
        agent=agent
    )

    crew = Crew(agents=[agent], tasks=[task])
    return str(crew.kickoff())


def run_grade(context: str, question: str, user_answer: str, model_name: str) -> str:
    llm = get_llm(model_name)

    agent = Agent(
        role="Medical Answer Grader",
        goal="Grade the student's answer using only provided context with citations.",
        backstory="You are a strict but helpful medical instructor.",
        llm=llm,
        allow_delegation=False,
    )

    task = Task(
        description=grade_prompt(context, question, user_answer),
        expected_output="A score + brief feedback + the correct answer grounded in provided context, include citations when available.",
        agent=agent
    )

    crew = Crew(agents=[agent], tasks=[task])
    return str(crew.kickoff())

def route_mode(mode: str) -> str:
    m = (mode or "").strip().lower()
    if m in ["explain", "quiz", "flashcards", "grade"]:
        return m
    return "explain"
