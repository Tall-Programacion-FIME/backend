from typing import Optional

from pydantic import BaseModel


class TokenBase(BaseModel):
    access_token: str


class Token(TokenBase):
    refresh_token: str


class TokenData(BaseModel):
    username: Optional[str] = None
