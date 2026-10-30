from sqlalchemy import Column, Integer, Text, Float, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.sql import func

from app.db.database import Base


class JobMatch(Base):
    __tablename__ = "job_matches"

    id = Column(Integer, primary_key=True, index=True)

    resume_id = Column(
        Integer,
        ForeignKey("resumes.id"),
        nullable=False
    )

    resume_version_id = Column(
        Integer,
        ForeignKey("resume_versions.id"),
        nullable=True
    )

    job_id = Column(
        Integer,
        ForeignKey("jobs.id"),
        nullable=False
    )

    match_score = Column(
        Float,
        nullable=False
    )

    matched_skills = Column(
        JSONB,
        nullable=False
    )

    missing_skills = Column(
        JSONB,
        nullable=False
    )

    strengths = Column(
        JSONB,
        nullable=False
    )

    weaknesses = Column(
        JSONB,
        nullable=False
    )

    recommendation = Column(
        Text,
        nullable=False
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )