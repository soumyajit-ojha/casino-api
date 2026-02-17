from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.core import security
from app.repositories.user_repository import UserRepository
from app.schemas.user_schema import UserCreate, Token


class AuthService:
    def __init__(self, db: Session):
        self.db = db
        self.user_repo = UserRepository(db)

    def register_user(self, user_in: UserCreate) -> Token:
        if self.user_repo.get_by_username(user_in.username):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already registered",
            )

        hashed_pw = security.get_password_hash(user_in.password)
        user = self.user_repo.create_user_with_wallet(user_in.username, hashed_pw)

        access_token = security.create_access_token(subject=user.id)
        return Token(access_token=access_token, token_type="bearer")

    def authenticate(self, username: str, password: str) -> Token:
        print("USERNAME", username)
        print("PASSWORD", password)
        user = self.user_repo.get_by_username(username)
        print("LOGIN USER", user)
        if not user or not security.verify_password(password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
            )

        access_token = security.create_access_token(subject=user.id)
        return Token(access_token=access_token, token_type="bearer")
