from sqlalchemy import Column, String
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


class Book(Base):
    __tablename__ = "books"

    id = Column(String(6), primary_key=True)
    title = Column(String(255), nullable=False)
    author = Column(String(255), nullable=False)

    def __repr__(self):
        return f"<Book(title='{self.title}', author='{self.author}', publication_year={self.publication_year})>"


class User(Base):
    __tablename__ = "users"

    id = Column(String(6), primary_key=True)
