from sqlalchemy.orm import Session
from app.resume_analysis.model import ResumeAnalysis as ResumeAnalysisModel

from app.resume.models import  Resume

class ResumeAnalysisRepository:

    def __init__(self,db:Session):
        self.db=db

    def create(self,analysis:ResumeAnalysisModel):
        self.db.add(analysis)
        self.db.commit()
        self.db.refresh(analysis)
        return analysis
    
    def get_latest_by_resume_id(self, resume_id: int):
        return (
            self.db.query(ResumeAnalysisModel)
            .filter(ResumeAnalysisModel.resume_id == resume_id)
            .order_by(ResumeAnalysisModel.created_at.desc())
            .first()
        )

    def get_all_by_user_id(self, user_id: int):
        return (
            self.db.query(ResumeAnalysisModel)
            .join(
                Resume,
                ResumeAnalysisModel.resume_id == Resume.id
            )
            .filter(Resume.user_id == user_id)
            .order_by(ResumeAnalysisModel.created_at.desc())
            .all()
        )


    