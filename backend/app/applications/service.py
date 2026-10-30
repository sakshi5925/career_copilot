
from app.applications.model import Application, ApplicationStatus
from app.applications.repository import ApplicationRepository
from app.job.repository import JobRepository
from app.resume.version_repository import ResumeVersionRepository
from datetime import datetime, timezone


class ApplicationService:
    def __init__(
        self,
        application_repository: ApplicationRepository,
        job_repository: JobRepository,
        version_repository: ResumeVersionRepository
    ):
        self.application_repository = application_repository
        self.job_repository = job_repository
        self.version_repository = version_repository

    def create_application(
        self,
        user_id: int,
        job_id: int | None = None,
        resume_version_id: int | None = None,
        status: ApplicationStatus = ApplicationStatus.SAVED,
        notes: str | None = None
    ):
        if job_id is not None:
            job = self.job_repository.get_by_id(job_id)

            if job is None or job.user_id != user_id:
                raise ValueError("Job not found")

        if resume_version_id is not None:
            version = self.version_repository.get_by_id_for_user(
                resume_version_id,
                user_id
            )

            if version is None:
                raise ValueError("Resume version not found")

        application = Application(
            user_id=user_id,
            job_id=job_id,
            resume_version_id=resume_version_id,
            status=status,
            notes=notes
        )

        return self.application_repository.create(application)

    def get_user_applications(self, user_id: int):
        return self.application_repository.get_all_by_user_id(user_id)

    def update_application_status(
        self,
        application_id: int,
        user_id: int,
        status: ApplicationStatus
    ):
        application = self.application_repository.get_by_id(application_id)

        if application is None or application.user_id != user_id:
            raise ValueError("Application not found")

        application.status = status

        if status == ApplicationStatus.APPLIED and application.applied_at is None:
            application.applied_at = datetime.now(timezone.utc)


        return self.application_repository.update(application)

    def delete_application(self, application_id: int, user_id: int):
        application = self.application_repository.get_by_id(application_id)

        if application is None or application.user_id != user_id:
            raise ValueError("Application not found")

        self.application_repository.delete(application)


    
    def update_application_notes(
        self,
        application_id: int,
        user_id: int,
        notes: str | None
    ):
        application = self.application_repository.get_by_id(application_id)

        if application is None or application.user_id != user_id:
            raise ValueError("Application not found")

        application.notes = notes

        return self.application_repository.update(application)
