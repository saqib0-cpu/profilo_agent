from fastapi import APIRouter
from app.api.schemas import ChatRequest, ChatResponse, LeadRequest
from app.graph import run_agent
from app.memory import get_history, update_history
from app.tools import save_lead
from app.data.projects import PROJECTS
from app.data.skills import SKILLS
from app.utils import clamp_text

router = APIRouter()


@router.get("/")
def root():
    return {"status": "Server Status: running"}


@router.get("/health")
def health():
    return {"status": "Healthy"}


@router.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    history = get_history(req.session_id)
    reply, updated_history = run_agent(clamp_text(req.message), history)
    update_history(req.session_id, updated_history)
    return ChatResponse(reply=reply)


@router.post("/lead")
def create_lead(req: LeadRequest):
    result = save_lead(name=req.name, email=req.email, phone=req.phone, message=req.message)
    return {"status": "saved", "detail": result}


@router.get("/projects")
def get_projects():
    return {"projects": PROJECTS}


@router.get("/skills")
def get_skills_route():
    return {"skills": SKILLS}