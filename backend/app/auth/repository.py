from sqlalchemy.orm import Session
from app.auth.model import User

class AuthRepository:
    def __init__(self,db:Session):
        self.db=db
    
    def create(self,name :str,email:str,password_hash:str):
        user= User(
            name=name,
            email=email,
            password_hash=password_hash
        )

        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)

        return user

    def get_by_email(self, email: str):

        return (
            self.db.query(User)
            .filter(User.email == email)
            .first()
        )   


