from sqlalchemy import Column, Integer, Text, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.sql import func

from app.db.database import Base


class JobAnalysis(Base):
    __tablename__ = "job_analyses"

    id = Column(Integer, primary_key=True, index=True)

    job_id = Column(
        Integer,
        ForeignKey("jobs.id"),
        nullable=False
    )

    summary = Column(Text, nullable=False)

    required_skills = Column(JSONB, nullable=False)

    preferred_skills = Column(JSONB, nullable=False)

    responsibilities = Column(JSONB, nullable=False)

    experience_required = Column(Text, nullable=True)

    education_required = Column(Text, nullable=True)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )