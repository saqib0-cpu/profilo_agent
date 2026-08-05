EXPERIENCE = [
    {
        "role": "ML Intern (Content Opportunity Scoring)",
        "org": "FlyRank AI Internship",
        "period": "2026",  # <-- update
        "description": (
            "Building baseline content-scoring systems, working with real "
            "anonymized data through structured weekly assignments."
        )
    },
    {
        "role": "AI Developer (Freelance / Project-based)",
        "org": "Techanion Pvt Ltd",
        "period": "",  # <-- update
        "description": (
            "Designed and built an agentic AI lead generation system using "
            "LangChain and LangGraph."
        )
    },
    # Add more roles below in the same format
]


def get_experience_text() -> str:
    lines = []
    for e in EXPERIENCE:
        period = f" ({e['period']})" if e["period"] else ""
        lines.append(f"{e['role']} — {e['org']}{period}: {e['description']}")
    return "\n".join(lines)