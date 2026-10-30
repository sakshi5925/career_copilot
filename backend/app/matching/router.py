
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Any
from app.auth.dependencies import get_current_user
from app.auth.model import User
from app.db.dependencies import get_db

from app.ai.service import AIService
from app.job.repository import JobRepository
from app.matching.model import JobMatch
from app.matching.repository import JobMatchRepository

from app.matching.schemas import ResumeMatchRankingResponse
from app.matching.service import MatchingService
from app.resume.version_repository import ResumeVersionRepository

router = APIRouter(prefix="/matching", tags=["Matching"])


def get_matching_service(
    db: Session = Depends(get_db)
):
    return MatchingService(
        version_repository=ResumeVersionRepository(db),
        job_repository=JobRepository(db),
        match_repository=JobMatchRepository(db),
        ai_service=AIService()
    )


@router.post("/", response_model=ResumeMatchRankingResponse, status_code=201)
def match_resume_to_job(
    job_id: int,
    current_user: User = Depends(get_current_user),
    service: MatchingService = Depends(get_matching_service)
) -> dict[str, Any]:
    try:
        return service.match_resume_to_job(
            job_id=job_id,
            user_id=current_user.id
        )
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc))
