from datetime import datetime

from pydantic import BaseModel

class ResumeAnalysisResponse(BaseModel):
    id: int
    resume_id: int
    score: int

    strengths: list[str]
    weaknesses: list[str]
    missing_skills: list[str]
    recommendations: list[str]

    created_at: datetime

    model_config = {
        "from_attributes": True
    }

    