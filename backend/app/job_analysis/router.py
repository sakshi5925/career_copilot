from fastapi import APIRouter, Depends, HTTPException

from app.auth.dependencies import get_current_user
from app.auth.model import User
from app.job_analysis.dependencies import get_job_analysis_service
from app.job_analysis.schemas import JobAnalysisResponse
from app.job_analysis.service import JobAnalysisService
from app.ai.exceptions import AIServiceError


router = APIRouter(
    prefix="/jobs",
    tags=["Job Analysis"]
)


@router.post(
    "/{job_id}/analyze",
    response_model=JobAnalysisResponse
)
def analyze_job(
    job_id: int,
    current_user: User = Depends(get_current_user),
    service: JobAnalysisService = Depends(
        get_job_analysis_service
    )
):
    try:
        return service.analyze_job(
            job_id=job_id,
            user_id=current_user.id
        )

    except ValueError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e)
        )

    except AIServiceError as e:
        raise HTTPException(
            status_code=503,
            detail=str(e)
        )


@router.get(
    "/{job_id}/analysis",
    response_model=JobAnalysisResponse
)
def get_latest_analysis(
    job_id: int,
    current_user: User = Depends(get_current_user),
    service: JobAnalysisService = Depends(
        get_job_analysis_service
    )
):
    try:
        analysis = service.get_latest_analysis(
            job_id=job_id,
            user_id=current_user.id
        )

        if analysis is None:
            raise HTTPException(
                status_code=404,
                detail="Job has not been analyzed yet"
            )

        return analysis

    except ValueError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e)
        )

@router.get(
    "/{job_id}/analyses",
    response_model=list[JobAnalysisResponse]
)
def get_analysis_history(
    job_id: int,
    current_user: User = Depends(get_current_user),
    service: JobAnalysisService = Depends(
        get_job_analysis_service
    )
):
    try:
        return service.get_all_analyses(
            job_id=job_id,
            user_id=current_user.id
        )

    except ValueError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e)
        )