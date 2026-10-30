from fastapi import APIRouter, Depends, HTTPException

from app.auth.dependencies import get_current_user
from app.auth.model import User
from app.job.dependencies import get_job_service
from app.job.schemas import (
    JobCreateRequest,
    JobResponse,
    JobUpdateRequest,
    JobStatusUpdateRequest
)
from app.job.service import JobService


router = APIRouter(
    prefix="/jobs",
    tags=["Jobs"]
)


@router.post("/", response_model=JobResponse)
def create_job(
    data: JobCreateRequest,
    current_user: User = Depends(get_current_user),
    service: JobService = Depends(get_job_service)
):
    try:
        return service.create_job(
            user_id=current_user.id,
            title=data.title,
            company=data.company,
            description=data.description,
            location=data.location,
            url=data.url
        )

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )


@router.get("/", response_model=list[JobResponse])
def get_my_jobs(
    current_user: User = Depends(get_current_user),
    service: JobService = Depends(get_job_service)
):
    return service.get_user_jobs(
        user_id=current_user.id
    )


@router.get("/{job_id}", response_model=JobResponse)
def get_job(
    job_id: int,
    current_user: User = Depends(get_current_user),
    service: JobService = Depends(get_job_service)
):
    try:
        return service.get_job(
            job_id=job_id,
            user_id=current_user.id
        )

    except ValueError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e)
        )


@router.delete("/{job_id}")
def delete_job(
    job_id: int,
    current_user: User = Depends(get_current_user),
    service: JobService = Depends(get_job_service)
):
    try:
        service.delete_job(
            job_id=job_id,
            user_id=current_user.id
        )

        return {
            "message": "Job deleted successfully"
        }

    except ValueError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e)
        )

@router.patch("/{job_id}", response_model=JobResponse)
def update_job(
    job_id: int,
    data: JobUpdateRequest,
    current_user: User = Depends(get_current_user),
    service: JobService = Depends(get_job_service)
):
    try:
        return service.update_job(
            job_id=job_id,
            user_id=current_user.id,
            title=data.title,
            company=data.company,
            description=data.description,
            location=data.location,
            url=data.url
        )

    except ValueError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e)
        )

@router.patch("/{job_id}/status", response_model=JobResponse)
def update_job_status(
    job_id: int,
    data: JobStatusUpdateRequest,
    current_user: User = Depends(get_current_user),
    service: JobService = Depends(get_job_service)
):
    try:
        return service.update_status(
            job_id=job_id,
            user_id=current_user.id,
            status=data.status
        )

    except ValueError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e)
        )