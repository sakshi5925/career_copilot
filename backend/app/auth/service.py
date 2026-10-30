from app.auth.repository import AuthRepository
from app.auth.security import hash_password, verify_password, create_access_token

class AuthService:
    def __init__(self,repository:AuthRepository):
        self.repository=repository

    def register(self,name:str,email:str,password:str):

        existing_user= self.repository.get_by_email(email)

        if existing_user is not None:
            raise ValueError("Email already registered")

        password_hash=hash_password(password)

        user=self.repository.create(
            name=name,
            email=email,
            password_hash=password_hash
        )

        return user

    def login(self, email: str, password: str):
        user = self.repository.get_by_email(email)

        if user is None:
            raise ValueError("Invalid email or password")

        if not verify_password(password,user.password_hash):
            raise ValueError("Invalid email or password")

        access_token = create_access_token(
        user_id=user.id
        )

        return {
            "access_token": access_token,
            "token_type": "bearer"
        }
