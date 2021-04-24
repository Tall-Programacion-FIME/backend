from app.db import Base
from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=False)
    is_admin = Column(Boolean, default=False)

    books_for_sale = relationship("Book", back_populates="owner")


class BannedUser(Base):
    __tablename__ = "banned_users"

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, index=True)
