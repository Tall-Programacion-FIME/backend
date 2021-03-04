from os import path
from uuid import uuid4

import app.crud as crud
import app.schemas as schemas
from app.core.settings import settings
from app.core.storage import client as storage_client
from app.core.utils import get_file_url
from fastapi import APIRouter, Depends, UploadFile, File, Form
from fastapi.security import OAuth2PasswordBearer
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session

from ...dependencies import get_db

router = APIRouter()


@router.post("/create_book", response_model=schemas.Book)
async def create_book(name: str = Form(...), author: str = Form(...), cover: UploadFile = File(...),
                      token: str = Depends(OAuth2PasswordBearer(tokenUrl="/token")),
                      authorize: AuthJWT = Depends(), db: Session = Depends(get_db)):
    authorize.jwt_required(token=token)
    current_user = authorize.get_jwt_subject()
    user = crud.get_user_by_email(db, email=current_user)
    _, file_extension = path.splitext(cover.filename)
    new_file_name = uuid4().hex + file_extension
    stored_image = storage_client.put_object(
        bucket_name=settings.BUCKET_NAME,
        object_name=new_file_name,
        data=cover.file,
        length=-1,
        content_type=cover.content_type,
        part_size=10 * 1024 * 1024
    )
    url = get_file_url(stored_image.object_name)
    book = schemas.BookCreate(name=name, author=author, cover_url=url)
    return crud.create_book(db, book=book, user_id=user.id)
