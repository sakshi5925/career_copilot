
from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.resume.schemas import ResumeSourceResponse



class ConversationCreate(BaseModel):
    title: str = "New conversation"
    resume_version_id: int | None = None

class MessageCreate(BaseModel):
    content: str


class ConversationResponse(BaseModel):
    id: int
    user_id: int
    title: str | None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class MessageResponse(BaseModel):
    id: int
    conversation_id: int
    role: str
    content: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ConversationChatResponse(BaseModel):
    user_message: MessageResponse
    assistant_message: MessageResponse
    sources: list[ResumeSourceResponse]