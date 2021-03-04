import app.schemas as schemas
from sqlalchemy.orm import Session
from app.db import models


def create_book(db: Session, book: schemas.BookCreate, user_id: int) -> schemas.Book:
    db_book = models.Book(**book.dict(), owner_id=user_id)
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book
