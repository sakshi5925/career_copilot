from pydantic import BaseModel


class ResumeUploadResponse(BaseModel):
    id: int
    user_id: int
    filename: str
    resume_version_id: int | None = None

    class Config:
        from_attributes = True

class ResumeChunkResponse(BaseModel):
    id: int
    resume_version_id: int
    chunk_index: int
    content: str
    chunk_metadata: dict | None
    embedding: list[float] | None

    class Config:
        from_attributes = True

class ResumeSourceResponse(BaseModel):
    id: int
    resume_version_id: int
    chunk_index: int
    content: str
    chunk_metadata: dict | None

    class Config:
        from_attributes = True

class ResumeQuestionResponse(BaseModel):
    answer: str
    