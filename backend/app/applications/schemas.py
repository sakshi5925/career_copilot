
from datetime import datetime
from pydantic import BaseModel, ConfigDict
from app.applications.model import ApplicationStatus


class ApplicationCreate(BaseModel):
    job_id: int | None = None
    resume_version_id: int | None = None
    status: ApplicationStatus = ApplicationStatus.SAVED
    notes: str | None = None

class ApplicationStatusUpdate(BaseModel):
    status: ApplicationStatus


class ApplicationResponse(BaseModel):
    id: int
    user_id: int
    job_id: int | None
    resume_version_id: int | None
    status: ApplicationStatus
    applied_at: datetime | None
    notes: str | None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ApplicationNotesUpdate(BaseModel):
    notes: str | None = None