from os import path
from typing import List
from uuid import uuid4

import app.crud as crud
import app.schemas as schemas
from app.core.settings import settings
from app.core.storage import client as storage_client
from app.core.utils import get_file_url
from elasticsearch import Elasticsearch
from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException, status, BackgroundTasks
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from fastapi_pagination import Page, PaginationParams, add_pagination
from fastapi_pagination.ext.sqlalchemy import paginate

from app.db import models
from ...dependencies import get_db, get_es, get_current_user

router = APIRouter()


@router.post("/create", response_model=schemas.Book, responses={
    400: {"description": "File type not supported"}
})
async def create_book(name: str = Form(...), author: str = Form(...), price: int = Form(...),
                      cover: UploadFile = File(...),
                      user: schemas.User = Depends(get_current_user),
                      db: Session = Depends(get_db),
                      es: Elasticsearch = Depends(get_es)):
    _, file_extension = path.splitext(cover.filename)
    if file_extension not in ['.jpeg', '.jpg', '.png']:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File type not supported"
        )
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
    book = schemas.BookCreate(name=name, author=author, cover_url=url, price=price)
    return crud.create_book(db, es, book=book, user_id=user.id)


@router.get("/", response_model=Page[schemas.Book])
def list_books(db: Session = Depends(get_db), params: PaginationParams = Depends()):
    return paginate(db.query(models.Book), params)


@router.get("/search/", response_model=List[schemas.Book])
def search_for_book(q: str, db: Session = Depends(get_db), es: Elasticsearch = Depends(get_es)):
    query = {
        "query": {
            "multi_match": {
                "query": f"{q}",
                "fields": ["name", "author"]
            }
        }
    }
    res = es.search(body=query, index="books")
    queried_books = res["hits"]["hits"]
    if len(queried_books) == 0:
        raise HTTPException(status_code=404, detail="No books found matching your query")
    results: List[schemas.Book] = []
    for book in queried_books:
        book_id = book["_source"]["id"]
        results.append(
            crud.get_book(db, book_id=book_id)
        )
    return results


@router.get("/{book_id}", response_model=schemas.Book)
def get_book(book_id: int, db: Session = Depends(get_db)):
    db_book = crud.get_book(db, book_id=book_id)
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return db_book


@router.post("/{book_id}", response_model=schemas.Book)
def update_book(book_id: int, book: schemas.BookUpdate, es: Elasticsearch = Depends(get_es),
                db: Session = Depends(get_db), user: schemas.User = Depends(get_current_user)):
    current_book = crud.get_book(db, book_id=book_id)
    if user.id != current_book.owner_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    book_db = crud.update_book(db=db, es=es, book=book, book_id=book_id)
    return book_db


@router.delete("/{book_id}")
def delete_book(background_tasks: BackgroundTasks, book_id: int, user: schemas.User = Depends(get_current_user),
                db: Session = Depends(get_db), es: Elasticsearch = Depends(get_es)):
    current_book = crud.get_book(db, book_id=book_id)
    if user.id != current_book.owner_id and not user.is_admin:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    crud.delete_book(background_tasks, db, es, book_id=book_id)
    return JSONResponse(
        status_code=200,
        content={"detail": "Book deleted"}
    )
