from app.db.database import SessionLocal
from app.resume_analysis.repository import ResumeAnalysisRepository


db = SessionLocal()

repository = ResumeAnalysisRepository(db)

result = repository.get_latest_by_resume_id(1)

if result:
    print("Latest Analysis:")
    print("ID:", result.id)
    print("Resume ID:", result.resume_id)
    print("Score:", result.score)
else:
    print("No analysis found")

db.close()