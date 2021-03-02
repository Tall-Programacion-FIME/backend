from datetime import timedelta, datetime
from typing import Optional

from sqlalchemy.orm import Session
from jose import JWTError, jwt

from app.crud import get_user_by_email
import app.schemas as schemas
from .passwords import verify_password
from . import settings


def authenticate_user(db: Session, email: str, password: str) -> Optional[schemas.User]:
    user = get_user_by_email(db, email=email)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt
