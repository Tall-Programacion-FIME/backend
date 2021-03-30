import random

from sqlalchemy.orm import Session
from elasticsearch import Elasticsearch
from faker import Faker

from app.tests.utils.user import create_random_user
from app.schemas.book import BookCreate
from app.crud.crud_book import create_book


def test_create_book(db: Session, es: Elasticsearch, fake: Faker) -> None:
    name = " ".join(fake.words(3))
    author = fake.name()
    cover_url = fake.image_url()
    price = random.randint(0, 500)
    book_in = BookCreate(name=name, author=author, cover_url=cover_url, price=price)
    user = create_random_user(db=db, fake=fake)
    book = create_book(db=db, es=es, book=book_in, user_id=user.id)
    assert book.name == name
    assert book.author == author
    assert book.cover_url == cover_url
    assert book.price == price
