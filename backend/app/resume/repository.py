from sqlalchemy.orm import Session

from app.resume.models import Resume


class ResumeRepository:

    def __init__(self, db: Session):
        self.db = db

    def create(self, user_id: int, filename: str, raw_text: str):

        resume = Resume(
            user_id=user_id,
            filename=filename,
            raw_text=raw_text
        )

        self.db.add(resume)
        self.db.commit()
        self.db.refresh(resume)

        return resume

    def get_by_id(self, resume_id: int):

        return (
            self.db.query(Resume)
            .filter(Resume.id == resume_id)
            .first()
        )

    def get_all_by_user(self, user_id: int):

        return (
            self.db.query(Resume)
            .filter(Resume.user_id == user_id)
            .order_by(Resume.created_at.desc())
            .all()
        )

    def update(self, resume_id: int, raw_text: str):

        resume = self.get_by_id(resume_id)

        if resume is None:
            return None

        resume.raw_text = raw_text

        self.db.commit()
        self.db.refresh(resume)

        return resume

    def delete(self, resume_id: int, user_id: int):
        resume = (
            self.db.query(Resume)
            .filter(
                Resume.id == resume_id,
                Resume.user_id == user_id
            )
            .first()
        )

        if resume is None:
            return False

        self.db.delete(resume)
        self.db.commit()

        return True

    def get_by_id_for_user(self, resume_id: int, user_id: int):

        return (
            self.db.query(Resume)
            .filter(
                Resume.id == resume_id,
                Resume.user_id == user_id
            )
            .first()
        )