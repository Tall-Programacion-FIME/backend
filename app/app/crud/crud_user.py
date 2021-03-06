import app.schemas as schemas
from app.core import passwords
from app.db import models
from sqlalchemy.orm import Session


def get_user(db: Session, user_id: int) -> schemas.User:
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str) -> schemas.User:
    return db.query(models.User).filter(models.User.email == email).first()


def create_user(db: Session, user: schemas.UserCreate) -> schemas.User:
    hashed_password = passwords.get_password_hash(user.password)
    db_user = models.User(email=user.email, name=user.name, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def delete_user(db: Session, user_id: int):
    user = get_user(db, user_id=user_id)
    db.delete(user)
    db.commit()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()
