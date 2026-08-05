SKILLS = {
    "Programming Languages": ["Python", "JavaScript", "SQL", "Dart"],
    "AI / ML": [
        "LangChain", "LangGraph", "TensorFlow", "PyTorch",
        "Prompt Engineering", "RAG systems", "Scikit-Learn", "OpenCV"
    ],
    "Backend": ["FastAPI", "REST API design", "MongoDB", "SQL Server"],
    "Frontend / Mobile": ["React", "Flutter", "HTML/CSS/JavaScript"],
    "Tools": ["Git", "GitHub", "Docker"],
}


def get_skills_text(category: str = "") -> str:
    category = (category or "").strip()
    if category:
        for cat, items in SKILLS.items():
            if category.lower() in cat.lower():
                return f"{cat}: {', '.join(items)}"

    lines = [f"{cat}: {', '.join(items)}" for cat, items in SKILLS.items()]
    return "\n".join(lines)