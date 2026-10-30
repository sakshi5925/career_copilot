from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Enum as SQLEnum
from enum import Enum as PyEnum
from sqlalchemy.sql import func

from app.db.database import Base
# need to change status ->and then run migration
class JobStatus(str, PyEnum):
    SAVED = "saved"
    INTERESTED = "interested"
    APPLIED = "applied"
    INTERVIEW = "interview"
    OFFER = "offer"
    REJECTED = "rejected"
    NOT_INTERESTED = "not_interested"


class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    title = Column(String(255), nullable=False)

    company = Column(String(255), nullable=False)

    location = Column(String(255), nullable=True)

    description = Column(Text, nullable=False)

    status = Column(
        SQLEnum(JobStatus),
        nullable=False,
        default=JobStatus.SAVED
    )

    url = Column(String(1000), nullable=True)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )