from sqlalchemy.orm import Session
from faker import Faker

from app.tests.utils.utils import random_email, random_lower_string
from app.schemas.user import UserCreate
from app.crud.crud_user import create_user


def test_create_user(db: Session, fake: Faker) -> None:
    email = random_email()
    password = random_lower_string()
    user_in = UserCreate(email=email, password=password, name=fake.name())
    user = create_user(db, user_in)
    assert user.email == email
    assert hasattr(user, "hashed_password")
