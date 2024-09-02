from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class Book(Base):
    __tablename__ = "books"

    id: Mapped[str] = mapped_column(String(6), primary_key=True)

    title: Mapped[str]
    author: Mapped[str]

    def __repr__(self):
        return f"<Book(title='{self.title}', author='{self.author}'>"


class User(Base):
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(String(6), primary_key=True)
