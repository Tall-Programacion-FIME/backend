from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session

from . import crud, schemas
from .db import SessionLocal, es

reusable_oauth2 = OAuth2PasswordBearer(tokenUrl="/auth/token")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_es():
    try:
        yield es
    finally:
        ...


def get_current_user(
    db: Session = Depends(get_db),
    token: str = Depends(reusable_oauth2),
    authorize: AuthJWT = Depends(),
) -> schemas.User:
    authorize.jwt_required(token=token)
    current_user_email = authorize.get_jwt_subject()
    user = crud.get_user_by_email(db, email=current_user_email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


def get_current_admin(
    current_user: schemas.User = Depends(get_current_user),
) -> schemas.User:
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Not enough privileges"
        )
    return current_user
