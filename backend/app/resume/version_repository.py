from sqlalchemy.orm import Session

from app.resume.version_model import ResumeVersion

from app.resume.models import Resume

class ResumeVersionRepository:

    def __init__(self, db: Session):
        self.db = db

    def create(self, version: ResumeVersion):
        self.db.add(version)
        self.db.commit()
        self.db.refresh(version)

        return version

    def get_by_id(self, version_id: int):
        return (
            self.db.query(ResumeVersion)
            .filter(ResumeVersion.id == version_id)
            .first()
        )

    def get_all_by_resume_id(self, resume_id: int):
        return (
            self.db.query(ResumeVersion)
            .filter(ResumeVersion.resume_id == resume_id)
            .order_by(ResumeVersion.version_number.desc())
            .all()
        )

    def get_latest_by_resume_id(self, resume_id: int):
        return (
            self.db.query(ResumeVersion)
            .filter(ResumeVersion.resume_id == resume_id)
            .order_by(ResumeVersion.version_number.desc())
            .first()
        )

    def get_by_id_for_user(self, version_id: int, user_id: int):
        return (
            self.db.query(ResumeVersion)
            .join(Resume, Resume.id == ResumeVersion.resume_id)
            .filter(
                ResumeVersion.id == version_id,
                Resume.user_id == user_id
            )
            .first()
        )

    def get_all_by_user_id(self, user_id: int):
        return (
            self.db.query(ResumeVersion)
            .join(Resume, Resume.id == ResumeVersion.resume_id)
            .filter(Resume.user_id == user_id)
            .order_by(ResumeVersion.created_at.desc())
            .all()
        )