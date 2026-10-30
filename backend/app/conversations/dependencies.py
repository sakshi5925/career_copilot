from fastapi import Depends
from sqlalchemy.orm   import Session
from app.db.dependencies import get_db
from app.conversations.repository import ConversationRepository
from app.conversations.message_repository import MessageRepository
from app.conversations.service import ConversationService
from app.resume.version_repository import ResumeVersionRepository
from app.resume.chunk_repository import ResumeChunkRepository
from app.resume.chunk_service import ResumeChunkService
from app.embeddings.service import EmbeddingService
from app.ai.service import AIService


def  get_conversation_service(
    db: Session =Depends(get_db)
)->ConversationService:

    conversation_repository=ConversationRepository(db)
    message_repository=MessageRepository(db)
    version_repository = ResumeVersionRepository(db)
    chunk_repository = ResumeChunkRepository(db)
    embedding_service = EmbeddingService()
    ai_service = AIService()

    resume_chunk_service = ResumeChunkService(
        chunk_repository=chunk_repository,
        version_repository=version_repository,
        embedding_service=embedding_service,
        ai_service=ai_service
    )

    return ConversationService(
        conversation_repository=conversation_repository,
        message_repository=message_repository,
        version_repository=version_repository,
        resume_chunk_service=resume_chunk_service
    )


