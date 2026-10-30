from datetime import datetime

from pydantic import BaseModel, Field


class JobMatchResult(BaseModel):
    match_score: float = Field(ge=0, le=100)

    matched_skills: list[str] = Field(default_factory=list)

    missing_skills: list[str] = Field(default_factory=list)

    strengths: list[str] = Field(default_factory=list)

    weaknesses: list[str] = Field(default_factory=list)

    recommendation: str


class JobMatchResponse(BaseModel):
    id: int
    resume_id: int
    resume_version_id: int | None = None
    resume_filename: str 
    job_id: int
    match_score: float
    matched_skills: list[str]
    missing_skills: list[str]
    strengths: list[str]
    weaknesses: list[str]
    recommendation: str
    created_at: datetime | None

    class Config:
        from_attributes = True

class ResumeMatchRankingResponse(BaseModel):
    job_id: int
    total_versions_compared: int
    best_match: JobMatchResponse
    all_matches: list[JobMatchResponse]