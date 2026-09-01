from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.response import APIResponse
from app.schemas.auth import LoginRequest, LogoutRequest, LoginResponse
from app.db.session import get_db
from app.services.auth import AuthService

from app.api.v1.dependencies import get_current_user, get_current_token


auth_router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

@auth_router.post("/login", response_model=APIResponse[LoginResponse])
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    
    data = AuthService.login(db = db, payload = payload)
    return APIResponse(
        status_code=status.HTTP_200_OK,
        message="Login successful",
        data=data,
        error=None
    )
    
@auth_router.post("/logout", response_model=APIResponse[None])
def logout(
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user),
    access_token: str = Depends(get_current_token)
):
    AuthService.logout(db, current_user=current_user, access_token=access_token)
    return APIResponse(
        status_code=status.HTTP_204_NO_CONTENT,
        message="Logout successful",
        data=None,
        error=None
    )