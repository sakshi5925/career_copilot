from sqlalchemy.orm import Session

from app.matching.model import JobMatch


class JobMatchRepository:

    def __init__(self, db: Session):
        self.db = db

    def create(self, match: JobMatch):
        self.db.add(match)
        self.db.commit()
        self.db.refresh(match)

        return match

    def get_latest_by_resume_and_job(
        self,
        resume_id: int,
        job_id: int
    ):
        return (
            self.db.query(JobMatch)
            .filter(
                JobMatch.resume_id == resume_id,
                JobMatch.job_id == job_id
            )
            .order_by(JobMatch.created_at.desc())
            .first()
        )

    def get_all_by_resume_and_job(
        self,
        resume_id: int,
        job_id: int
    ):
        return (
            self.db.query(JobMatch)
            .filter(
                JobMatch.resume_id == resume_id,
                JobMatch.job_id == job_id
            )
            .order_by(JobMatch.created_at.desc())
            .all()
        )

    def get_by_version_and_job(
        self,
        resume_version_id: int,
        job_id: int
    ):
        return (
            self.db.query(JobMatch)
            .filter(
                JobMatch.resume_version_id == resume_version_id,
                JobMatch.job_id == job_id
            )
            .first()
        )
