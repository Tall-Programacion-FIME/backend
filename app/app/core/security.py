from typing import Optional

from sqlalchemy.orm import Session
from jose import JWTError, jwt
from .passwords import verify_password

from app.crud import get_user_by_email
import app.schemas as schemas


def authenticate_user(db: Session, email: str, password: str) -> Optional[schemas.User]:
    user = get_user_by_email(db, email=email)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user
