from .db import SessionLocal, es


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_es():
    try:
        yield es
    finally:
        ...
