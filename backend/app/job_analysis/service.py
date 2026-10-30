from app.ai.service import AIService
from app.job.repository import JobRepository
from app.job_analysis.model import JobAnalysis
from app.job_analysis.repository import JobAnalysisRepository



class JobAnalysisService:
    def __init__(
        self,
        job_repository: JobRepository,
        analysis_repository: JobAnalysisRepository,
        ai_service: AIService,
    ):
        self.job_repository = job_repository
        self.analysis_repository = analysis_repository
        self.ai_service = ai_service
   
    
    def analyze_job(self, job_id: int, user_id: int):
        job = self.job_repository.get_by_id_for_user(
            job_id=job_id,
            user_id=user_id
        )

        if job is None:
            raise ValueError("Job not found")

        analysis = self.ai_service.analyze_job(
            job_description=job.description
        )

        db_analysis = JobAnalysis(
            job_id=job.id,
            summary=analysis.summary,
            required_skills=analysis.required_skills,
            preferred_skills=analysis.preferred_skills,
            responsibilities=analysis.responsibilities,
            experience_required=analysis.experience_required,
            education_required=analysis.education_required,
        )

        return self.analysis_repository.create(db_analysis)

    def get_latest_analysis(
        self,
        job_id: int,
        user_id: int
    ):
        job = self.job_repository.get_by_id_for_user(
            job_id=job_id,
            user_id=user_id
        )

        if job is None:
            raise ValueError("Job not found")

        return self.analysis_repository.get_latest_by_job_id(
            job_id
        )

    def get_all_analyses(
        self,
        job_id: int,
        user_id: int
    ):
        job = self.job_repository.get_by_id_for_user(
            job_id=job_id,
            user_id=user_id
        )

        if job is None:
            raise ValueError("Job not found")

        return self.analysis_repository.get_all_by_job_id(
            job_id
        )


