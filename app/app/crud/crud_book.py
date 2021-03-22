from typing import List

import app.schemas as schemas
from app.core.settings import settings
from app.core.storage import client as storage_client
from app.db import models
from elasticsearch import Elasticsearch
from fastapi import BackgroundTasks
from sqlalchemy.orm import Session


def create_book(db: Session, es: Elasticsearch, book: schemas.BookCreate, user_id: int) -> schemas.Book:
    db_book = models.Book(**book.dict(), owner_id=user_id)
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    es_book = {
        "name": book.name,
        "author": book.author,
        "id": db_book.id,
    }
    es.index(index="books", body=es_book)
    return db_book


def update_book(db: Session, es: Elasticsearch, book: schemas.BookUpdate, book_id: int) -> schemas.Book:
    db_book: models.Book = db.query(models.Book).filter(models.Book.id == book_id).first()
    db_book.name = book.name
    db_book.author = book.author
    db_book.price = book.price
    db.commit()
    es_book_id = get_book_elastic_id(es, book_id)
    es.update(index="books", id=es_book_id, body={
        "doc": {
            "name": book.name,
            "author": book.author
        }
    })
    return db_book


def delete_book(background_tasks: BackgroundTasks, db: Session, es: Elasticsearch, book_id: int):
    db_book: models.Book = db.query(models.Book).filter(models.Book.id == book_id).first()
    es_book_id = get_book_elastic_id(es, book_id)
    s3_url = db_book.cover_url
    s3_name = s3_url.split("/")[-1]
    background_tasks.add_task(storage_client.remove_object, settings.BUCKET_NAME, s3_name)
    background_tasks.add_task(es.delete, index="books", id=es_book_id)
    db.delete(db_book)
    db.commit()


def get_book(db: Session, book_id: int) -> schemas.Book:
    return db.query(models.Book).filter(models.Book.id == book_id).first()


def get_all_books(db: Session, skip: int = 0, limit: int = 100) -> List[schemas.Book]:
    return db.query(models.Book).offset(skip).limit(limit).all()


def get_book_elastic_id(es: Elasticsearch, book_id: int) -> str:
    es_book = es.search(index="books", body={
        "query": {
            "match": {
                "id": book_id
            }
        },
        "size": 1
    })
    es_book_id = es_book["hits"]["hits"][0]["_id"]
    return es_book_id
