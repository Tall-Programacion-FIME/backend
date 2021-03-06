from typing import List

import app.crud as crud
import app.schemas as schemas
from app.core import utils
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from ...dependencies import get_db, get_current_user, get_current_admin

router = APIRouter()


@router.get("/", response_model=List[schemas.User])
def list_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db),
               user: schemas.User = Depends(get_current_admin)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@router.post("/", response_model=schemas.User, responses={
    403: {"description": "Not a valid email domain"},
    400: {"description": "Email already registered"}
})
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    if not utils.is_valid_email_domain(user.email):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not a valid email domain")
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
    return crud.create_user(db=db, user=user)


@router.get("/me", response_model=schemas.User)
def read_users_me(user=Depends(get_current_user)):
    return user


@router.get("/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return db_user


@router.delete("/{user_id}/ban")
def ban_user(user_id: int, db: Session = Depends(get_db), admin: schemas.User = Depends(get_current_admin)):
    user = crud.get_user(db, user_id=user_id)
    crud.ban_user(db, user_email=user.email)
    return JSONResponse(status_code=200, content={"detail": "User banned"})
