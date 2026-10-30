from sqlalchemy.orm import Session

from app.job_analysis.model import JobAnalysis


class JobAnalysisRepository:

    def __init__(self, db: Session):
        self.db = db

    def create(self, analysis: JobAnalysis):
        self.db.add(analysis)
        self.db.commit()
        self.db.refresh(analysis)

        return analysis

    def get_latest_by_job_id(self, job_id: int):
        return (
            self.db.query(JobAnalysis)
            .filter(JobAnalysis.job_id == job_id)
            .order_by(JobAnalysis.created_at.desc())
            .first()
        )

    def get_all_by_job_id(self, job_id: int):
        return (
            self.db.query(JobAnalysis)
            .filter(JobAnalysis.job_id == job_id)
            .order_by(JobAnalysis.created_at.desc())
            .all()
        )