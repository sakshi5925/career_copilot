from app.db.database import engine, Base
from app.resume.models import Resume


Base.metadata.create_all(bind=engine)

print("Tables created successfully! ✅")