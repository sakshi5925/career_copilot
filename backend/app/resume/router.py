from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
import tempfile
import os
from app.resume.service import ResumeService
from app.ai.exceptions import AIServiceError
from app.resume.dependencies import get_resume_service
from app.resume_analysis.schemas import ResumeAnalysisResponse
from app.resume.schemas import (
    ResumeUploadResponse,
    ResumeChunkResponse,
    ResumeSourceResponse,
    ResumeQuestionResponse
)
from app.resume.chunk_service import ResumeChunkService
from app.resume.dependencies import get_resume_chunk_service
from app.auth.dependencies import get_current_user
from app.auth.model import User



router = APIRouter(
    prefix="/resumes",
    tags=["Resumes"]
)


@router.post("/upload",response_model=ResumeUploadResponse)
def upload_resume(
    file:UploadFile=File(...),
    current_user: User = Depends(get_current_user),
    service:ResumeService =Depends(get_resume_service)
):
    temp_path = None

    try:
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=os.path.splitext(file.filename)[1]
        ) as temp_file:

            temp_file.write(file.file.read())
            temp_path=temp_file.name

        result= service.upload_resume(
            user_id=current_user.id,
            filename=file.filename,
            file_path=temp_path
        )

        return result

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
    
    finally:
        if temp_path and os.path.exists(temp_path):
            os.remove(temp_path)


@router.delete("/{resume_id}")
def remove_resume(
    resume_id: int,
    current_user: User = Depends(get_current_user),
    service: ResumeService = Depends(get_resume_service)
):
    try:
        response = service.remove_resume(
            resume_id=resume_id,
            user_id=current_user.id
        )

        if not response:
            raise HTTPException(
                status_code=404,
                detail="Resume not found"
            )

        return {"message": "Resume deleted successfully"}

    except ValueError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e)
        )

@router.post("/{resume_id}/analyze", response_model=ResumeAnalysisResponse)
def analyze_resume(
    resume_id: int,
    current_user: User = Depends(get_current_user),
    service: ResumeService = Depends(get_resume_service)
):

    try:
        result = service.analyze_resume(
            resume_id=resume_id,
            user_id=current_user.id
        )

        return result

    except ValueError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e)
        )
    except AIServiceError as e:
        raise HTTPException(
            status_code=503,
            detail=str(e)
        )

@router.get("/{resume_id}/analysis", response_model=ResumeAnalysisResponse)
def analysis_resume(
    resume_id: int,
    current_user: User = Depends(get_current_user),
    service: ResumeService = Depends(get_resume_service)
):  
    try:
        result=service.get_latest_analysis(resume_id,user_id=current_user.id)
        return result

    except ValueError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e)
        )

   
@router.get(
    "/{resume_id}/analyses",
    response_model=list[ResumeAnalysisResponse]
)
def get_analysis_history(
    resume_id: int,
    current_user: User = Depends(get_current_user),
    service: ResumeService = Depends(get_resume_service)
):  
    try:
      
        return service.get_all_analyses(resume_id,user_id=current_user.id)

    except ValueError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e)
        )


@router.post(
    "/versions/{resume_version_id}/chunks",
    response_model=list[ResumeChunkResponse]
)
def create_resume_chunks(
    resume_version_id: int,
    current_user: User = Depends(get_current_user),
    service: ResumeChunkService = Depends(get_resume_chunk_service)
):
    try:
        return service.create_chunks_for_version(
            resume_version_id=resume_version_id,
            user_id=current_user.id
        )

    except ValueError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e)
        )


@router.get(
    "/versions/{resume_version_id}/search",
    response_model=list[ResumeChunkResponse]
)
def search_resume_chunks(
    resume_version_id: int,
    query: str,
    limit: int = 5,
    current_user: User = Depends(get_current_user),
    service: ResumeChunkService = Depends(get_resume_chunk_service)
):
    try:
        return service.search_similar_chunks(
            resume_version_id=resume_version_id,
            user_id=current_user.id,
            query=query,
            limit=limit
        )
    except ValueError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e)
        )


@router.get(
    "/versions/{resume_version_id}/ask",
    response_model=ResumeQuestionResponse
)
def ask_resume_question(
    resume_version_id: int,
    query: str,
    limit: int = 5,
    current_user: User = Depends(get_current_user),
    service: ResumeChunkService = Depends(get_resume_chunk_service)
):
    try:
        return service.answer_question(
            resume_version_id=resume_version_id,
            user_id=current_user.id,
            question=query,
            limit=limit
        )
    except ValueError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e)
        )


@router.get(
    "/analyses/history",
    response_model=list[ResumeAnalysisResponse]
)
def get_user_analysis_history(
    current_user: User = Depends(get_current_user),
    service: ResumeService = Depends(get_resume_service)
):
    return service.get_all_user_analyses(
        user_id=current_user.id
    )


@router.get("/", response_model=list[ResumeUploadResponse])
def get_user_resumes(
    current_user: User = Depends(get_current_user),
    service: ResumeService = Depends(get_resume_service)
):
    return service.get_user_resumes(user_id=current_user.id)

