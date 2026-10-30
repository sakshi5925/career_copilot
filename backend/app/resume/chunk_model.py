from sqlalchemy import (
    Column,
    Integer,
    Text,
    DateTime,
    ForeignKey
)
from sqlalchemy.dialects.postgresql import JSONB
from pgvector.sqlalchemy import Vector
from sqlalchemy.sql import func

from app.db.database import Base


class ResumeChunk(Base):
    __tablename__ = "resume_chunks"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    resume_version_id = Column(
        Integer,
        ForeignKey(
            "resume_versions.id",
            ondelete="CASCADE"
        ),
        nullable=False
    )

    chunk_index = Column(
        Integer,
        nullable=False
    )

    content = Column(
        Text,
        nullable=False
    )

    chunk_metadata = Column(
        JSONB,
        nullable=True
    )

    embedding = Column(
        Vector(384),
        nullable=True
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )