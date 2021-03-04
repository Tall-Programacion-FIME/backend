from typing import List

import app.schemas as schemas
from app.db import models
from sqlalchemy.orm import Session


def create_book(db: Session, book: schemas.BookCreate, user_id: int) -> schemas.Book:
    db_book = models.Book(**book.dict(), owner_id=user_id)
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book


def get_book(db: Session, book_id: int) -> schemas.Book:
    return db.query(models.Book).filter(models.Book.id == book_id).first()


def get_all_books(db: Session, skip: int = 0, limit: int = 100) -> List[schemas.Book]:
    return db.query(models.Book).offset(skip).limit(limit).all()
