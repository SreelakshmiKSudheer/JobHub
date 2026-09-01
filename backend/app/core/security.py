from __future__ import annotations

import hashlib
import secrets
from datetime import datetime, timedelta, timezone

import jwt
from passlib.context import CryptContext

from enum import Enum

from app.core.config import settings

class Role(str, Enum):
    USER = "user"
    ADMIN = "admin"
    
class TokenType(str, Enum):
    ACCESS = "access"
    REFRESH = "refresh"

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def _build_jwt_token_payload(user_id: str, token_type: str, role: Role, version: int,expires_delta: timedelta, extra_payload: dict[str, object] | None = None) -> dict[str, object]:
    now = datetime.now(timezone.utc)
    
    payload: dict[str, object] = {
        "sub": user_id,
        "type": token_type,
        "role": role,
        "iat": int(now.timestamp()),
        "exp": int((now + expires_delta).timestamp()),
        "version": version
    }
    if extra_payload:
        payload.update(extra_payload)
    return payload

def create_access_token(user_id: str, role: Role, extra_payload: dict[str, object] | None = None) -> str:
    payload = _build_jwt_token_payload(user_id=user_id, token_type=TokenType.ACCESS,
    role=role, expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES), extra_payload=extra_payload)
    return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.JWT_ALGORITHM)

def decode_token(token: str) -> dict[str, object]:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise ValueError("Token has expired")
    except jwt.InvalidTokenError:
        raise ValueError("Invalid token")
    
def hash_token(token: str) -> str:
    return hashlib.sha256(token.encode("utf-8")).hexdigest()