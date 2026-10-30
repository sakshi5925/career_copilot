from app.db.database import SessionLocal

from app.resume.repository import ResumeRepository
from app.ai.service import AIService

from app.resume_analysis.repository import ResumeAnalysisRepository

from app.resume.service import ResumeService


db = SessionLocal()

resume_repository = ResumeRepository(db)

ai_service = AIService()

analysis_repository = ResumeAnalysisRepository(db)


resume_service = ResumeService(
    repository=resume_repository,
    ai_service=ai_service,
    analysis_repository=analysis_repository
)


result = resume_service.analyze_resume(1)


print("Analysis saved successfully!")

print("ID:", result.id)
print("Resume ID:", result.resume_id)
print("Score:", result.score)

print("Strengths:", result.strengths)
print("Weaknesses:", result.weaknesses)
print("Missing Skills:", result.missing_skills)
print("Recommendations:", result.recommendations)


db.close()