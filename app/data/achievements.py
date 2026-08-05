ACHIEVEMENTS = [
    # {"title": "Top student — HVAC/DB course, etc.", "year": "2025", "description": ""},
    # Add your real achievements here
]


def get_achievements_text() -> str:
    if not ACHIEVEMENTS:
        return "No achievements added yet."
    lines = [f"{a['title']} ({a['year']}): {a.get('description', '')}" for a in ACHIEVEMENTS]
    return "\n".join(lines)
    #1. Activate your virtual environment first
#.\venv\Scripts\activate

# 2. Run the application as a module
#python -m app.run