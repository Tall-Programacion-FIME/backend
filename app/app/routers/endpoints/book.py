from os import path
from tempfile import TemporaryFile
from typing import List
from uuid import uuid4

import app.crud as crud
import app.schemas as schemas
from app.core.settings import settings
from app.core.storage import s3 as storage_client
from app.core.utils import get_file_url
from app.db import models
from fastapi import (
    APIRouter,
    BackgroundTasks,
    Depends,
    File,
    Form,
    HTTPException,
    UploadFile,
    status,
)
from fastapi.responses import JSONResponse
from fastapi_pagination import Page, PaginationParams, add_pagination
from fastapi_pagination.ext.sqlalchemy import paginate
from PIL import Image
from sqlalchemy.orm import Session

from ...dependencies import get_current_user, get_db

router = APIRouter()


@router.post(
    "/create",
    response_model=schemas.Book,
    responses={400: {"description": "File type not supported"}},
)
async def create_book(
    name: str = Form(...),
    author: str = Form(...),
    price: int = Form(...),
    cover: UploadFile = File(...),
    user: schemas.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    _, file_extension = path.splitext(cover.filename)
    if file_extension not in [".jpeg", ".jpg", ".png"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="File type not supported"
        )
    new_file_name = uuid4().hex + file_extension

    a = TemporaryFile()
    file_extension = file_extension.strip(".")
    if file_extension == "jpg":
        file_extension = "jpeg"
    resizing_image = Image.open(cover.file)
    resizing_image = resizing_image.resize((656, 912), Image.ANTIALIAS)
    resizing_image.save(a, format=file_extension, quality=95)
    a.seek(0)

    storage_client.put_object(
        Bucket=settings.BUCKET_NAME,
        Key=new_file_name,
        Body=a,
        ContentType=cover.content_type,
        ACL="public-read",
    )
    url = get_file_url(new_file_name)
    book = schemas.BookCreate(name=name, author=author, cover_url=url, price=price)
    return crud.create_book(db, book=book, user_id=user.id)


@router.get("/", response_model=Page[schemas.Book])
def list_books(db: Session = Depends(get_db), params: PaginationParams = Depends()):
    return paginate(db.query(models.Book).order_by(models.Book.id.desc()), params)


@router.get("/{book_id}", response_model=schemas.Book)
def get_book(book_id: int, db: Session = Depends(get_db)):
    db_book = crud.get_book(db, book_id=book_id)
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return db_book


@router.post("/{book_id}", response_model=schemas.Book)
def update_book(
    book_id: int,
    book: schemas.BookUpdate,
    db: Session = Depends(get_db),
    user: schemas.User = Depends(get_current_user),
):
    current_book = crud.get_book(db, book_id=book_id)
    if user.id != current_book.owner_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    book_db = crud.update_book(db=db, book=book, book_id=book_id)
    return book_db


@router.delete("/{book_id}")
def delete_book(
    background_tasks: BackgroundTasks,
    book_id: int,
    user: schemas.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    current_book = crud.get_book(db, book_id=book_id)
    if user.id != current_book.owner_id and not user.is_admin:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    crud.delete_book(background_tasks, db, book_id=book_id)
    return JSONResponse(status_code=200, content={"detail": "Book deleted"})
