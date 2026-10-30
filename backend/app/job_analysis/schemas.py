from datetime import datetime

from pydantic import BaseModel, Field


class JobAnalysisResult(BaseModel):
    summary: str

    required_skills: list[str] = Field(default_factory=list)

    preferred_skills: list[str] = Field(default_factory=list)

    responsibilities: list[str] = Field(default_factory=list)

    experience_required: str | None = None

    education_required: str | None = None


class JobAnalysisResponse(BaseModel):
    id: int
    job_id: int
    summary: str
    required_skills: list[str]
    preferred_skills: list[str]
    responsibilities: list[str]
    experience_required: str | None
    education_required: str | None
    created_at: datetime | None

    class Config:
        from_attributes = True