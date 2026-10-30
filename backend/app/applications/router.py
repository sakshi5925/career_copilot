
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_user
from app.auth.model import User
from app.db.dependencies import get_db

from app.applications.model import ApplicationStatus
from app.applications.repository import ApplicationRepository
from app.applications.service import ApplicationService
from app.applications.schemas import (
    ApplicationCreate,
    ApplicationStatusUpdate,
    ApplicationResponse,
)
from app.applications.schemas import ApplicationNotesUpdate
from app.job.repository import JobRepository
from app.resume.version_repository import ResumeVersionRepository


router = APIRouter(
    prefix="/applications",
    tags=["Applications"]
)


def get_application_service(
    db: Session = Depends(get_db)
) -> ApplicationService:
    return ApplicationService(
        application_repository=ApplicationRepository(db),
        job_repository=JobRepository(db),
        version_repository=ResumeVersionRepository(db)
    )


@router.post("/", response_model=ApplicationResponse, status_code=201)
def create_application(
    data: ApplicationCreate,
    current_user: User = Depends(get_current_user),
    service: ApplicationService = Depends(get_application_service)
):
    try:
        return service.create_application(
            user_id=current_user.id,
            job_id=data.job_id,
            resume_version_id=data.resume_version_id,
            status=data.status,
            notes=data.notes
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/", response_model=list[ApplicationResponse])
def get_applications(
    current_user: User = Depends(get_current_user),
    service: ApplicationService = Depends(get_application_service)
):
    return service.get_user_applications(current_user.id)


@router.patch(
    "/{application_id}/status",
    response_model=ApplicationResponse
)
def update_application_status(
    application_id: int,
    data: ApplicationStatusUpdate,
    current_user: User = Depends(get_current_user),
    service: ApplicationService = Depends(get_application_service)
):
    try:
        return service.update_application_status(
            application_id=application_id,
            user_id=current_user.id,
            status=data.status
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/{application_id}", status_code=204)
def delete_application(
    application_id: int,
    current_user: User = Depends(get_current_user),
    service: ApplicationService = Depends(get_application_service)
):
    try:
        service.delete_application(application_id, current_user.id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))



@router.patch("/{application_id}/notes", response_model=ApplicationResponse)
def update_application_notes(
    application_id: int,
    payload: ApplicationNotesUpdate,
    current_user: User = Depends(get_current_user),
    service: ApplicationService = Depends(get_application_service),
):
    try:
        return service.update_application_notes(
            application_id=application_id,
            user_id=current_user.id,
            notes=payload.notes,
        )
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc))
