from pydantic import BaseModel, Field

class ResumeAnalysis(BaseModel):
    score: int = Field(ge=0, le=100)
    strengths: list[str]
    weaknesses: list[str]
    missing_skills: list[str]
    recommendations: list[str]

class ResumeAnalyzeRequest(BaseModel):
    resume_text: str
    


class ResumeQuestionResponse(BaseModel):
    answer: str