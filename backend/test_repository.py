from app.db.database import SessionLocal
from app.resume.repository import ResumeRepository

db =SessionLocal();

try:

    repository=ResumeRepository(db)

    # resume=repository.create(
    #     user_id=1,
    #     filename="test_resume.txt",
    #     raw_text="Python developer with FastAPI and PostgreSQL experience."
    # )

    # print("Created resume:")
    # print(resume.id)
    # print(resume.filename)
    # print(resume.raw_text)

    resume=repository.delete(2)


finally:
    db.close()