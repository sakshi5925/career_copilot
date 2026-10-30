from app.ai.service import AIService


ai_service = AIService()

resume_text = """
Sakshi Kumar
B.Tech Information Technology

Skills:
Python, FastAPI, PostgreSQL, React

Projects:
Built an AI Career Copilot using FastAPI and React.
"""

result = ai_service.analyze_resume(resume_text)

print(result)
print(type(result))