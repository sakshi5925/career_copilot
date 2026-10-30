from sqlalchemy.orm import Session

from app.job.model import Job


class JobRepository:

    def __init__(self, db: Session):
        self.db = db

    def create(
        self,
        user_id: int,
        title: str,
        company: str,
        description: str,
        location: str | None = None,
        url: str | None = None,
    ):
        job = Job(
            user_id=user_id,
            title=title,
            company=company,
            description=description,
            location=location,
            url=url,
        )

        self.db.add(job)
        self.db.commit()
        self.db.refresh(job)

        return job

    def get_by_id(self, job_id: int):
        return (
            self.db.query(Job)
            .filter(Job.id == job_id)
            .first()
        )

    def get_by_id_for_user(self, job_id: int, user_id: int):
        return (
            self.db.query(Job)
            .filter(
                Job.id == job_id,
                Job.user_id == user_id
            )
            .first()
        )

    def get_all_by_user(self, user_id: int):
        return (
            self.db.query(Job)
            .filter(Job.user_id == user_id)
            .order_by(Job.created_at.desc())
            .all()
        )

    def delete(self, job_id: int):
        job = self.get_by_id(job_id)

        if job is None:
            return False

        self.db.delete(job)
        self.db.commit()

        return True


    def update(
        self,
        job_id: int,
        title: str | None = None,
        company: str | None = None,
        description: str | None = None,
        location: str | None = None,
        url: str | None = None,
    ):
        job = self.get_by_id(job_id)

        if job is None:
            return None

        if title is not None:
            job.title = title

        if company is not None:
            job.company = company

        if description is not None:
            job.description = description

        if location is not None:
            job.location = location

        if url is not None:
            job.url = url

        self.db.commit()
        self.db.refresh(job)

        return job