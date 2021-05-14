from app.db import Base
from sqlalchemy import Column, ForeignKey, Integer, Numeric, String, Boolean
from sqlalchemy.orm import relationship


class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    author = Column(String)
    cover_url = Column(String)
    price = Column(Numeric, nullable=False)
    sold = Column(Boolean, default=False)
    marked_for_delete = Column(Boolean, default=False)

    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="books_for_sale")
