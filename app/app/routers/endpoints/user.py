import datetime
from typing import List

import app.crud as crud
import app.schemas as schemas
import jwt
from app.core import utils
from app.core.settings import settings
from app.dependencies import get_es
from elasticsearch import Elasticsearch
from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from ...core.utils import send_verification_email
from ...dependencies import get_current_admin, get_current_user, get_db
from ...schemas import VerificationToken

router = APIRouter()


@router.get("/", response_model=List[schemas.User])
def list_users(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    user: schemas.User = Depends(get_current_admin),
):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@router.post(
    "/",
    response_model=schemas.User,
    responses={400: {"description": "Registration error"}},
)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    if not utils.is_valid_email_domain(user.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Correo invalido"
        )
    db_user = crud.get_user_by_email(db, email=user.email)
    banned_user = crud.get_banned_user(db, email=user.email)
    if banned_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Has sido baneado."
        )
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ya existe una cuenta con ese correo",
        )

    created_user = crud.create_user(db=db, user=user)
    token_data = VerificationToken(
        user_id=created_user.id,
        exp=datetime.datetime.utcnow() + datetime.timedelta(weeks=4),
    )
    token = jwt.encode(token_data.dict(), settings.authjwt_secret_key)
    send_verification_email(token)
    return created_user


@router.get("/me", response_model=schemas.User)
def read_users_me(user=Depends(get_current_user)):
    return user


@router.get("/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return db_user


@router.delete("/{user_id}/ban")
def ban_user(
    background_tasks: BackgroundTasks,
    user_id: int,
    db: Session = Depends(get_db),
    es: Elasticsearch = Depends(get_es),
    admin: schemas.User = Depends(get_current_admin),
):
    user = crud.get_user(db, user_id=user_id)
    crud.ban_user(
        background_tasks=background_tasks, db=db, es=es, user_email=user.email
    )
    return JSONResponse(status_code=200, content={"detail": "User banned"})
