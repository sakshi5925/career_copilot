from sqlalchemy.orm import Session
from app.applications.model import Application

class ApplicationRepository:

    def __init__(self, db: Session):
        self.db = db

    def create(self, application: Application):
        self.db.add(application)
        self.db.commit()
        self.db.refresh(application)
        return application

    def get_by_id(self, application_id: int):
        return (
            self.db.query(Application)
            .filter(Application.id == application_id)
            .first()
        )

    def get_all_by_user_id(self, user_id: int):
        return (
            self.db.query(Application)
            .filter(Application.user_id == user_id)
            .order_by(Application.created_at.desc())
            .all()
        )

    def update(self, application: Application):
        self.db.commit()
        self.db.refresh(application)
        return application

    def delete(self, application: Application):
        self.db.delete(application)
        self.db.commit()