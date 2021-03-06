from typing import List

from pydantic import BaseModel

from .book import Book


class UserBase(BaseModel):
    name: str
    email: str


class UserCreate(UserBase):
    password: str


class UserToken(BaseModel):
    email: str
    password: str


class User(UserBase):
    id: int
    is_active: bool
    is_admin: bool
    books_for_sale: List[Book]

    class Config:
        orm_mode = True


class BannedUser(BaseModel):
    id: int
    email: str

    class Config:
        orm_mode = True
