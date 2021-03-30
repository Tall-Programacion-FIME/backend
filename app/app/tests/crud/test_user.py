from sqlalchemy.orm import Session
from faker import Faker

from app.tests.utils.utils import random_email, random_lower_string
from app.schemas.user import UserCreate
from app.core.security import authenticate_user
from app.crud.crud_user import create_user


def test_create_user(db: Session, fake: Faker) -> None:
    email = random_email()
    password = random_lower_string()
    name = fake.name()
    user_in = UserCreate(email=email, password=password, name=name)
    user = create_user(db, user_in)
    assert user.email == email
    assert hasattr(user, "hashed_password")


def test_authenticate_user(db: Session, fake: Faker) -> None:
    email = random_email()
    password = random_lower_string()
    name = fake.name()
    user_in = UserCreate(email=email, password=password, name=name)
    user = create_user(db, user_in)
    authenticated_user = authenticate_user(db, email=email, password=password)
    assert authenticated_user
    assert user.email == authenticated_user.email


def test_not_authenticate_user(db: Session) -> None:
    email = random_email()
    password = random_lower_string()
    user = authenticate_user(db, email=email, password=password)
    assert user is None
