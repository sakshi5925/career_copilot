from fastapi import APIRouter, Depends, HTTPException
from app.auth.schemas import (
    RegisterRequest,
    RegisterResponse,
    LoginRequest,
    TokenResponse
)
from app.auth.service import AuthService
from app.auth.dependencies import get_auth_service
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

@router.post("/register",response_model=RegisterResponse)
def register(request:RegisterRequest,service: AuthService = Depends(get_auth_service)):
    try:
        return service.register(
            name=request.name,
            email=request.email,
            password=request.password
        )
        
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )   


@router.post("/login",response_model=TokenResponse)
def login(form_data: OAuth2PasswordRequestForm = Depends(),service:AuthService=Depends(get_auth_service)):
    try:
        return service.login(
            email=form_data.username,
            password=form_data.password
        )

    except ValueError as e:
            raise HTTPException(
                status_code=401,
                detail=str(e)
            )    