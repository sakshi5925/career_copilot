from app.job.repository import JobRepository

from app.job.model import JobStatus

class JobService:

    def __init__(self, repository: JobRepository):
        self.repository = repository

    def create_job(
        self,
        user_id: int,
        title: str,
        company: str,
        description: str,
        location: str | None = None,
        url: str | None = None,
    ):
        if not title.strip():
            raise ValueError("Job title cannot be empty")

        if not company.strip():
            raise ValueError("Company name cannot be empty")

        if not description.strip():
            raise ValueError("Job description cannot be empty")

        return self.repository.create(
            user_id=user_id,
            title=title,
            company=company,
            description=description,
            location=location,
            url=url,
        )

    def get_job(self, job_id: int, user_id: int):
        job = self.repository.get_by_id_for_user(
            job_id=job_id,
            user_id=user_id
        )

        if job is None:
            raise ValueError("Job not found")

        return job

    def get_user_jobs(self, user_id: int):
        return self.repository.get_all_by_user(user_id)

    def delete_job(self, job_id: int, user_id: int):
        job = self.repository.get_by_id_for_user(
            job_id=job_id,
            user_id=user_id
        )

        if job is None:
            raise ValueError("Job not found")

        return self.repository.delete(job_id)


    def update_job(
        self,
        job_id: int,
        user_id: int,
        title: str | None = None,
        company: str | None = None,
        description: str | None = None,
        location: str | None = None,
        url: str | None = None,
    ):
        job = self.repository.get_by_id_for_user(
            job_id=job_id,
            user_id=user_id
        )

        if job is None:
            raise ValueError("Job not found")

        if title is not None and not title.strip():
            raise ValueError("Job title cannot be empty")

        if company is not None and not company.strip():
            raise ValueError("Company name cannot be empty")

        if description is not None and not description.strip():
            raise ValueError("Job description cannot be empty")

        return self.repository.update(
            job_id=job_id,
            title=title,
            company=company,
            description=description,
            location=location,
            url=url
        )

    def update_status(
        self,
        job_id: int,
        user_id: int,
        status: JobStatus
    ):
        job = self.repository.get_by_id_for_user(
            job_id=job_id,
            user_id=user_id
        )

        if job is None:
            raise ValueError("Job not found")

        job.status = status

        self.repository.db.commit()
        self.repository.db.refresh(job)

        return job