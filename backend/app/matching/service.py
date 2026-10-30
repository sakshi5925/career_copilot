from app.ai.service import AIService
from app.job.repository import JobRepository
from app.matching.model import JobMatch
from app.matching.repository import JobMatchRepository
# from app.resume.repository import ResumeRepository
from app.resume.version_repository import ResumeVersionRepository

class MatchingService:
    def __init__(
        self,
        version_repository: ResumeVersionRepository,
        job_repository: JobRepository,
        match_repository: JobMatchRepository,
        ai_service: AIService
    ):
        self.version_repository = version_repository
        self.job_repository = job_repository
        self.match_repository = match_repository
        self.ai_service = ai_service

    
    def match_resume_to_job(
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

        resume_versions = self.version_repository.get_all_by_user_id(
            user_id=user_id
        )

        if not resume_versions:
            raise ValueError(
                "No resume versions found. Please upload a resume first."
            )

        results = []

        for resume_version in resume_versions:
            db_match = self.match_repository.get_by_version_and_job(
                resume_version_id=resume_version.id,
                job_id=job.id
            )

            if db_match is None:
                match = self.ai_service.match_resume_to_job(
                    resume_text=resume_version.raw_text,
                    job_description=job.description
                )

                db_match = JobMatch(
                    resume_id=resume_version.resume_id,
                    resume_version_id=resume_version.id,
                    job_id=job.id,
                    match_score=match.match_score,
                    matched_skills=match.matched_skills,
                    missing_skills=match.missing_skills,
                    strengths=match.strengths,
                    weaknesses=match.weaknesses,
                    recommendation=match.recommendation
                )

                db_match = self.match_repository.create(db_match)

            results.append({
                "id": db_match.id,
                "resume_id": db_match.resume_id,
                "resume_version_id": resume_version.id,
                "resume_filename": resume_version.resume.filename,
                "job_id": db_match.job_id,
                "match_score": db_match.match_score,
                "matched_skills": db_match.matched_skills,
                "missing_skills": db_match.missing_skills,
                "strengths": db_match.strengths,
                "weaknesses": db_match.weaknesses,
                "recommendation": db_match.recommendation,
                "created_at": db_match.created_at
            })

        results.sort(
            key=lambda item: item["match_score"],
            reverse=True
        )

        return {
            "job_id": job.id,
            "total_versions_compared": len(results),
            "best_match": results[0],
            "all_matches": results
        }
