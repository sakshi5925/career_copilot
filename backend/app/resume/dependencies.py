
from sqlalchemy.orm import Session
from fastapi import Depends

from app.db.dependencies import get_db

from app.resume.repository import ResumeRepository
from app.resume_analysis.repository import ResumeAnalysisRepository
from app.resume.version_repository import ResumeVersionRepository
from app.resume.chunk_repository import ResumeChunkRepository

from app.resume.service import ResumeService
from app.resume.chunk_service import ResumeChunkService

from app.ai.service import AIService
from app.file_parser.service import FileParser
from app.embeddings.service import EmbeddingService


def get_resume_chunk_service(db: Session = Depends(get_db)):
    chunk_repository = ResumeChunkRepository(db)
    version_repository = ResumeVersionRepository(db)
    embedding_service = EmbeddingService()
    ai_service = AIService()

    return ResumeChunkService(
        chunk_repository=chunk_repository,
        version_repository=version_repository,
        embedding_service=embedding_service,
        ai_service=ai_service
    )


def get_resume_service(db: Session = Depends(get_db)):
    repository = ResumeRepository(db)
    analysis_repository = ResumeAnalysisRepository(db)
    version_repository = ResumeVersionRepository(db)
    ai_service = AIService()
    file_parser = FileParser()

    # Create the chunk service using the same database session
    chunk_service = ResumeChunkService(
        chunk_repository=ResumeChunkRepository(db),
        version_repository=version_repository,
        embedding_service=EmbeddingService(),
        ai_service=ai_service
    )

    return ResumeService(
        repository=repository,
        ai_service=ai_service,
        analysis_repository=analysis_repository,
        file_parser=file_parser,
        version_repository=version_repository,
        chunk_service=chunk_service
    )
