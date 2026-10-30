from app.db.database import SessionLocal
from app.resume.models import Resume
from app.resume_analysis.model import ResumeAnalysis
from app.resume_analysis.repository import ResumeAnalysisRepository


db = SessionLocal()

repository = ResumeAnalysisRepository(db)

analysis = ResumeAnalysis(
    resume_id=1,
    score=75,
    strengths=[
        "Python",
        "FastAPI",
        "PostgreSQL"
    ],
    weaknesses=[
        "Limited cloud experience"
    ],
    missing_skills=[
        "Docker",
        "AWS"
    ],
    recommendations=[
        "Build a Dockerized application",
        "Learn AWS fundamentals"
    ]
)

result = repository.create(analysis)

print("Created analysis:")
print(result.id)
print(result.score)

db.close()