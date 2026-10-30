from app.resume.repository import ResumeRepository
from app.ai.service import AIService
from app.resume_analysis.repository import ResumeAnalysisRepository
from app.resume_analysis.model import ResumeAnalysis as ResumeAnalysisModel
from app.resume.version_model import ResumeVersion
from app.resume.version_repository import ResumeVersionRepository
from app.file_parser.service import FileParser
from app.resume.chunk_service import ResumeChunkService

    
class ResumeService:

    def __init__(self, repository: ResumeRepository, ai_service: AIService,analysis_repository: ResumeAnalysisRepository,file_parser: FileParser, version_repository: ResumeVersionRepository, chunk_service: ResumeChunkService):
        self.repository = repository
        self.ai_service = ai_service
        self.analysis_repository = analysis_repository
        self.file_parser = file_parser
        self.version_repository=version_repository
        self.chunk_service = chunk_service


    def analyze_resume(self, resume_id: int,user_id: int):
        
        resume = self.repository.get_by_id_for_user(
            resume_id,
            user_id
        )

        if resume is None:
            raise ValueError("Resume not found")
        
        analysis=self.ai_service.analyze_resume(resume.raw_text)

        db_analysis = ResumeAnalysisModel(
            resume_id=resume.id,
            score=analysis.score,
            strengths=analysis.strengths,
            weaknesses=analysis.weaknesses,
            missing_skills=analysis.missing_skills,
            recommendations=analysis.recommendations
        )

        saved_analysis = self.analysis_repository.create(db_analysis)

        return saved_analysis


    def get_latest_analysis(self, resume_id: int,user_id:int):
        resume = self.repository.get_by_id_for_user(
            resume_id,
            user_id
        )


        if resume is None:
            raise ValueError("Resume not found")

        analysis=self.analysis_repository.get_latest_by_resume_id(resume_id)

        return analysis

    def get_all_analyses(self, resume_id: int, user_id: int):
        resume = self.repository.get_by_id_for_user(
            resume_id,
            user_id
        )

        if resume is None:
            raise ValueError("Resume not found")

        return self.analysis_repository.get_all_by_resume_id(resume_id)


    def upload_resume(
        self,
        user_id: int,
        filename: str,
        file_path: str
    ):
        # 1. Check whether this user already uploaded a file
        existing_resumes = self.repository.get_all_by_user(user_id)

        for existing_resume in existing_resumes:
            if existing_resume.filename.lower() == filename.lower():
                print("Resume already exists. Skipping upload.")

                # Find the latest version
                latest_version = max(
                    existing_resume.versions,
                    key=lambda v: v.version_number,
                    default=None
                )

                existing_resume.resume_version_id = (
                    latest_version.id if latest_version else None
                )

                return existing_resume

        # 2. Extract text from the file
        text = self.file_parser.parse(file_path)

        if not text or not text.strip():
            raise ValueError("Could not extract text from the resume.")

        # 3. Save the resume
        resume = self.repository.create(
            user_id=user_id,
            filename=filename,
            raw_text=text
        )

        # 4. Create the first resume version
        version = ResumeVersion(
            resume_id=resume.id,
            version_number=1,
            raw_text=text
        )

        version = self.version_repository.create(version)

        # 5. Create and save chunks with embeddings
        chunks = self.chunk_service.create_chunks_for_version(
            resume_version_id=version.id,
            user_id=user_id
        )

        print(f"Resume uploaded successfully. Chunks created: {len(chunks)}")

        # 6. Return the uploaded resume
        resume.resume_version_id = version.id

        return resume


    def remove_resume(self, resume_id: int, user_id: int):
        return self.repository.delete(
            resume_id=resume_id,
            user_id=user_id
        )

    def get_all_user_analyses(self, user_id: int):
        return self.analysis_repository.get_all_by_user_id(user_id)


    def get_user_resumes(self, user_id: int):
        resumes = self.repository.get_all_by_user(user_id)
        result = []

        for resume in resumes:
            versions = resume.versions

            latest_version = max(
                versions,
                key=lambda v: v.version_number,
                default=None,
            )

            result.append({
                "id": resume.id,
                "user_id": resume.user_id,
                "filename": resume.filename,
                "resume_version_id": (
                    latest_version.id if latest_version else None
                ),
            })

        return result