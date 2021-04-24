import app.schemas as schemas
from app.core import passwords
from app.db import models
from elasticsearch import Elasticsearch
from fastapi import BackgroundTasks
from sqlalchemy.orm import Session

from .crud_book import delete_user_books


def get_user(db: Session, user_id: int) -> schemas.User:
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str) -> schemas.User:
    return db.query(models.User).filter(models.User.email == email).first()


def get_banned_user(db: Session, email: str) -> schemas.BannedUser:
    return db.query(models.BannedUser).filter(models.BannedUser.email == email).first()


def create_user(db: Session, user: schemas.UserCreate) -> schemas.User:
    hashed_password = passwords.get_password_hash(user.password)
    db_user = models.User(
        email=user.email, name=user.name, hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def delete_user(
    background_tasks: BackgroundTasks, db: Session, es: Elasticsearch, user_id: int
):
    user = get_user(db, user_id=user_id)
    user_books = user.books_for_sale
    background_tasks.add_task(
        delete_user_books,
        background_tasks=background_tasks,
        db=db,
        es=es,
        books=user_books,
    )
    db.delete(user)
    db.commit()


def ban_user(
    background_tasks: BackgroundTasks, db: Session, es: Elasticsearch, user_email: str
):
    user = get_user_by_email(db, email=user_email)
    delete_user(background_tasks, db, es, user_id=user.id)
    db_banned_user = models.BannedUser(email=user_email)
    db.add(db_banned_user)
    db.commit()
    db.refresh(db_banned_user)


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()
