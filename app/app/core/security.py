from typing import Optional

import app.schemas as schemas
from app.crud import get_user_by_email
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from .passwords import verify_password

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/user/get_token")


def authenticate_user(db: Session, email: str, password: str) -> Optional[schemas.User]:
    user = get_user_by_email(db, email=email)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user
