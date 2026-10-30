from pydantic import BaseModel, Field
from app.job.model import JobStatus


class JobStatusUpdateRequest(BaseModel):
    status: JobStatus

class JobCreateRequest(BaseModel):
    title: str = Field(min_length=1, max_length=255)
    company: str = Field(min_length=1, max_length=255)
    description: str = Field(min_length=1)
    location: str | None = Field(default=None, max_length=255)
    url: str | None = Field(default=None, max_length=1000)


class JobResponse(BaseModel):
    id: int
    user_id: int
    title: str
    company: str
    description: str
    status: JobStatus
    location: str | None
    url: str | None

    class Config:
        from_attributes = True


class JobUpdateRequest(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=255)
    company: str | None = Field(default=None, min_length=1, max_length=255)
    description: str | None = Field(default=None, min_length=1)
    location: str | None = Field(default=None, max_length=255)
    url: str | None = Field(default=None, max_length=1000)