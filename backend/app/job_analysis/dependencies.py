from fastapi import Depends
from sqlalchemy.orm import Session

from app.ai.service import AIService
from app.db.dependencies import get_db
from app.job.repository import JobRepository
from app.job_analysis.repository import JobAnalysisRepository
from app.job_analysis.service import JobAnalysisService


def get_job_repository(
    db: Session = Depends(get_db)
):
    return JobRepository(db)


def get_job_analysis_repository(
    db: Session = Depends(get_db)
):
    return JobAnalysisRepository(db)


def get_ai_service():
    return AIService()

def get_job_analysis_service(
    job_repository: JobRepository = Depends(get_job_repository),
    analysis_repository: JobAnalysisRepository = Depends(
        get_job_analysis_repository
    ),
    ai_service: AIService = Depends(get_ai_service)
):
    return JobAnalysisService(
        job_repository=job_repository,
        analysis_repository=analysis_repository,
        ai_service=ai_service
    )