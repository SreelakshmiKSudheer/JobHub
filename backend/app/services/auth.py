from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.core.security import decode_token, verify_password, create_access_token
from app.schemas.auth import LoginRequest, LoginResponse, LogoutRequest
from app.repository.user import get_user_by_email, update_user_last_login, increment_user_token_version
from app.models import user


class AuthService:

    @staticmethod
    def login(db: Session, payload: LoginRequest) -> LoginResponse:
        
        user = get_user_by_email(db, payload.email)
        
        if not user or not verify_password(payload.password, user.password_hash):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")
        
        update_user_last_login(db, user)
        
        access_token = create_access_token(user_id=str(user.id), role=user.role, version=user.token_version)
        
        return LoginResponse(access_token=access_token, token_type="bearer")
    
    @staticmethod
    def logout(db: Session, current_user: user.User, access_token: str) -> None:
        
        payload = decode_token(access_token)
        increment_user_token_version(db, current_user)