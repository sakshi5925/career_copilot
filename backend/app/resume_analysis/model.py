from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base


class ResumeAnalysis(Base):
    __tablename__ = "resume_analyses"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True
    )

    resume_id: Mapped[int] = mapped_column(
        ForeignKey("resumes.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    score: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

    strengths: Mapped[list] = mapped_column(
        JSON,
        nullable=False
    )

    weaknesses: Mapped[list] = mapped_column(
        JSON,
        nullable=False
    )

    missing_skills: Mapped[list] = mapped_column(
        JSON,
        nullable=False
    )

    recommendations: Mapped[list] = mapped_column(
        JSON,
        nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    resume = relationship(
        "Resume",
        back_populates="analyses"
    )