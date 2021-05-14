from typing import List

import app.schemas as schemas
from app.core.settings import settings
from app.core.storage import s3 as storage_client
from app.db import models
from fastapi import BackgroundTasks
from sqlalchemy.orm import Session


def create_book(db: Session, book: schemas.BookCreate, user_id: int) -> schemas.Book:
    db_book = models.Book(**book.dict(), owner_id=user_id)
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book


def update_book(db: Session, book: schemas.BookUpdate, book_id: int) -> schemas.Book:
    db_book: models.Book = (
        db.query(models.Book).filter(models.Book.id == book_id).first()
    )
    db_book.name = book.name
    db_book.author = book.author
    db_book.price = book.price
    db.commit()
    return db_book


def sell_book(db: Session, book_id: int):
    db_book: models.Book = (
        db.query(models.Book).filter(models.Book.id == book_id).first()
    )
    db_book.sold = True
    db.commit()


def delete_book(background_tasks: BackgroundTasks, db: Session, book_id: int):
    db_book: models.Book = (
        db.query(models.Book).filter(models.Book.id == book_id).first()
    )
    s3_url = db_book.cover_url
    s3_name = s3_url.split("/")[-1]
    background_tasks.add_task(
        storage_client.delete_object, Bucket=settings.BUCKET_NAME, Key=s3_name
    )
    db.delete(db_book)
    db.commit()


def delete_user_books(
    background_tasks: BackgroundTasks,
    db: Session,
    books: List[schemas.Book],
):
    for book in books:
        background_tasks.add_task(
            delete_book,
            background_tasks=background_tasks,
            db=db,
            book_id=book.id,
        )


def get_book(db: Session, book_id: int) -> schemas.Book:
    return db.query(models.Book).filter(models.Book.id == book_id).first()


def get_all_books(db: Session, skip: int = 0, limit: int = 100) -> List[schemas.Book]:
    return db.query(models.Book).offset(skip).limit(limit).all()
