from app.crud.crud_user import create_user
from app.schemas.user import User, UserCreate
from app.tests.utils.utils import random_email, random_lower_string
from faker import Faker
from sqlalchemy.orm import Session


def create_random_user(db: Session, fake: Faker) -> User:
    email = random_email()
    password = random_lower_string()
    name = fake.name()
    user_in = UserCreate(email=email, password=password, name=name)
    user = create_user(db, user_in)
    return user
