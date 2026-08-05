# Edit this list with your real projects. Add as many as you want —
# the search_portfolio tool loops over all of them.

PROJECTS = [
    {
        "name": "Agentic AI Lead Generation System",
        "client": "Techanion Pvt Ltd",
        "category": "Agentic AI",
        "description": (
            "An autonomous agent pipeline that finds, qualifies, and scores leads "
            "using LLM-driven reasoning, cutting manual research time significantly."
        ),
        "stack": ["LangChain", "LangGraph", "Python", "FastAPI"],
        "link": ""
    },
    {
        "name": "PrimeFix",
        "client": "Saudi market home services app",
        "category": "Mobile App",
        "description": (
            "Bilingual Arabic/English mobile app connecting customers with home "
            "service providers in the Saudi market."
        ),
        "stack": ["Flutter", "Firebase"],
        "link": ""
    },
    {
        "name": "Zam Zam Nimko Inventory System",
        "client": "Small business client",
        "category": "Full-Stack Web App",
        "description": (
            "Full-stack inventory management system for stock tracking, sales "
            "records, and reporting for a food manufacturing business."
        ),
        "stack": ["React", "FastAPI", "SQL Server"],
        "link": ""
    },
    {
        "name": "AI Portfolio Assistant",
        "client": "Personal project",
        "category": "Agentic AI",
        "description": (
            "This very assistant — a LangGraph agent powered by Gemini that "
            "answers visitor questions and captures leads, embedded on this site."
        ),
        "stack": ["LangGraph", "Gemini API", "FastAPI", "JavaScript"],
        "link": ""
    },
    # Add more projects below, same format:
    # {
    #     "name": "",
    #     "client": "",
    #     "category": "",
    #     "description": "",
    #     "stack": [],
    #     "link": ""
    # },
]


def search_projects(query: str = "") -> str:
    """Returns all projects, optionally filtered by a keyword match."""
    query = (query or "").lower().strip()
    matches = PROJECTS
    if query:
        matches = [
            p for p in PROJECTS
            if query in p["name"].lower()
            or query in p["category"].lower()
            or query in p["description"].lower()
            or any(query in s.lower() for s in p["stack"])
        ]
        if not matches:
            matches = PROJECTS  # fall back to showing everything

    lines = []
    for p in matches:
        lines.append(
            f"- {p['name']} ({p['category']}, for {p['client']}): {p['description']} "
            f"[Stack: {', '.join(p['stack'])}]"
        )
    return "\n".join(lines)