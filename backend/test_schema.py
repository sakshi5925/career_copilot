from app.ai.schemas import ResumeAnalysis
from app.ai.service import AIService

analysis = ResumeAnalysis(
    score=80,
    strengths=["Python", "FastAPI"],
    weaknesses=["Limited AWS experience"],
    missing_skills=["Docker"],
    recommendations=["Add measurable results to projects"]
)

#print(analysis)

service = AIService()

service.analyze_resume(
    "Python developer with experience in FastAPI and PostgreSQL."
)