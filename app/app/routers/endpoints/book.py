import app.crud as crud
import app.schemas as schemas
from fastapi import APIRouter, Depends, UploadFile, File, Form
from fastapi.security import OAuth2PasswordBearer
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session

from ...dependencies import get_db

router = APIRouter()


@router.post("/create_book", response_model=schemas.Book)
def create_book(name: str = Form(...), author: str = Form(...), cover: UploadFile = File(...),
                token: str = Depends(OAuth2PasswordBearer(tokenUrl="/token")),
                authorize: AuthJWT = Depends(), db: Session = Depends(get_db)):
    # TODO save to S3
    authorize.jwt_required(token=token)
    current_user = authorize.get_jwt_subject()
    user = crud.get_user_by_email(db, email=current_user)
    book = schemas.BookCreate(name=name, author=author, cover_url=cover.filename)
    return crud.create_book(db, book=book, user_id=user.id)
