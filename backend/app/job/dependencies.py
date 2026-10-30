from fastapi import Depends
from sqlalchemy.orm import Session

from app.db.dependencies import get_db
from app.job.repository import JobRepository
from app.job.service import JobService


def get_job_repository(
    db: Session = Depends(get_db)
):
    return JobRepository(db)


def get_job_service(
    repository: JobRepository = Depends(get_job_repository)
):
    return JobService(repository)