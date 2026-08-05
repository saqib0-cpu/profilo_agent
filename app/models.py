from pydantic import BaseModel


class ChatRequest(BaseModel):
    message: str
    session_id: str = "default"


class ChatResponse(BaseModel):
    reply: str


class LeadRequest(BaseModel):
    name: str
    email: str = ""
    phone: str = ""
    message: str = ""