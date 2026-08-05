import json
import os
from datetime import datetime
# pyrefly: ignore [missing-import]
from google.genai import types

from app.data.projects import search_projects
from app.data.skills import get_skills_text
from app.data.profile import PROFILE, get_profile_text
from app.data.experience import get_experience_text
from app.data.education import get_education_text

LEADS_FILE = os.path.join(os.path.dirname(__file__), "data", "leads.json")


# ---------- Tool implementations ----------

def search_portfolio(query: str = "") -> str:
    """Searches profile summary, projects, education, and experience for a query."""
    parts = [
        get_profile_text(),
        "\nProjects:\n" + search_projects(query),
        "\nExperience:\n" + get_experience_text(),
        "\nEducation:\n" + get_education_text(),
    ]
    return "\n".join(parts)


def get_skills(category: str = "") -> str:
    """Returns Saqib's technical skills, optionally filtered by category."""
    return get_skills_text(category)


def get_resume_link() -> str:
    """Returns the link to Saqib's downloadable resume."""
    return f"You can download the resume here: {PROFILE['resume_url']}"


def save_lead(name: str, email: str = "", phone: str = "", message: str = "") -> str:
    """Saves a visitor's contact info as a lead for Saqib to follow up on."""
    entry = {
        "name": name,
        "email": email,
        "phone": phone,
        "message": message,
        "timestamp": datetime.utcnow().isoformat(),
    }

    leads = []
    if os.path.exists(LEADS_FILE):
        try:
            with open(LEADS_FILE, "r") as f:
                leads = json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            leads = []

    leads.append(entry)
    with open(LEADS_FILE, "w") as f:
        json.dump(leads, f, indent=2)

    return f"Thanks {name}! Your details have been saved — Saqib will get back to you soon."


TOOL_FUNCTIONS = {
    "search_portfolio": search_portfolio,
    "get_skills": get_skills,
    "get_resume_link": get_resume_link,
    "save_lead": save_lead,
}


# ---------- Gemini function declarations ----------

FUNCTION_DECLARATIONS = [
    types.FunctionDeclaration(
        name="search_portfolio",
        description=(
            "Search Saqib's portfolio (profile, projects, education, experience) "
            "for information relevant to the visitor's question. Use this for any "
            "question about who Saqib is or what he has built."
        ),
        parameters=types.Schema(
            type="OBJECT",
            properties={
                "query": types.Schema(
                    type="STRING",
                    description="Keyword describing what the visitor wants to know, e.g. 'machine learning projects'"
                )
            },
        ),
    ),
    types.FunctionDeclaration(
        name="get_skills",
        description="Get Saqib's technical skills, optionally filtered by category (e.g. 'AI', 'Backend').",
        parameters=types.Schema(
            type="OBJECT",
            properties={
                "category": types.Schema(type="STRING", description="Optional skill category filter")
            },
        ),
    ),
    types.FunctionDeclaration(
        name="get_resume_link",
        description="Get the link to download Saqib's resume. Use when the visitor asks for a resume/CV.",
        parameters=types.Schema(type="OBJECT", properties={}),
    ),
    types.FunctionDeclaration(
        name="save_lead",
        description=(
            "Save a visitor's contact details when they want to hire Saqib or "
            "want him to reach out. Call only once you have at least a name and "
            "an email or phone number."
        ),
        parameters=types.Schema(
            type="OBJECT",
            properties={
                "name": types.Schema(type="STRING", description="Visitor's name"),
                "email": types.Schema(type="STRING", description="Visitor's email"),
                "phone": types.Schema(type="STRING", description="Visitor's phone number"),
                "message": types.Schema(type="STRING", description="Project details / what they want"),
            },
            required=["name"],
        ),
    ),
]

TOOLS = [types.Tool(function_declarations=FUNCTION_DECLARATIONS)]