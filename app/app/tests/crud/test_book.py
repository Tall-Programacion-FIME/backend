import random

from app.crud.crud_book import create_book
from app.schemas.book import BookCreate
from app.tests.utils.user import create_random_user
from faker import Faker
from sqlalchemy.orm import Session


def test_create_book(db: Session, fake: Faker) -> None:
    name = " ".join(fake.words(3))
    author = fake.name()
    cover_url = fake.image_url()
    price = random.randint(0, 500)
    book_in = BookCreate(name=name, author=author, cover_url=cover_url, price=price)
    user = create_random_user(db=db, fake=fake)
    book = create_book(db=db, book=book_in, user_id=user.id)
    assert book.name == name
    assert book.author == author
    assert book.cover_url == cover_url
    assert book.price == price
