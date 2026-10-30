from fastapi import FastAPI
# from app.db.database import Base ,engine
from fastapi.middleware.cors import CORSMiddleware
from app.auth.model import User
from app.resume.router import router as resume_router
from app.resume_analysis.model import ResumeAnalysis
from app.auth.router import router as auth_router
from app.job.router import router as job_router
from app.job_analysis.router import router as job_analysis_router
from app.applications.router import router as application_router
from app.matching.router import router as matching_router
from app.conversations.router import router as conversations_router

# Base.metadata.create_all(bind=engine)

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Career Copilot API"}


app.include_router(resume_router)
app.include_router(auth_router)
app.include_router(job_router)
app.include_router(job_analysis_router)
app.include_router(conversations_router)
app.include_router(application_router)

app.include_router(matching_router)