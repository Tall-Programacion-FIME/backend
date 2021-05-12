from typing import Generator

import pytest
from app.db import SessionLocal
from app.main import app
from faker import Faker
from fastapi.testclient import TestClient


@pytest.fixture(scope="session")
def db() -> Generator:
    yield SessionLocal()


@pytest.fixture(scope="module")
def client() -> Generator:
    with TestClient(app) as c:
        yield c


@pytest.fixture(scope="module")
def fake() -> Generator:
    yield Faker()
