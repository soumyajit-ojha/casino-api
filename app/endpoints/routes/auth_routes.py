from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.endpoints import deps
from app.schemas.user_schema import UserCreate, LoginRequest, AuthResponse, Token
from app.services.auth_service import AuthService

router = APIRouter()


@router.post("/register", response_model=AuthResponse)
def register(payload: UserCreate, db: Session = Depends(deps.get_db)):
    auth_service = AuthService(db)
    token_data = auth_service.register_user(payload)

    return {
        "success": True,
        "message": "User registered successfully with starter balance",
        "data": {
            "access_token": token_data.access_token,
            "token_type": token_data.token_type,
        },
    }


@router.post("/login", response_model=AuthResponse)
def login(payload: LoginRequest, db: Session = Depends(deps.get_db)):
    auth_service = AuthService(db)
    token_data = auth_service.authenticate(payload.username, payload.password)

    return {
        "success": True,
        "message": "Login successful",
        "data": {
            "access_token": token_data.access_token,
            "token_type": token_data.token_type,
        },
    }
