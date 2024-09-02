from sqlalchemy import DateTime, ForeignKey, String, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from datetime import datetime
from typing import Optional


class Base(DeclarativeBase):
    pass


class Book(Base):
    __tablename__ = "books"

    id: Mapped[str] = mapped_column(String(6), primary_key=True)

    title: Mapped[str]
    author: Mapped[str]

    borrowings: Mapped[list["Borrowing"]] = relationship(back_populates="book")

    def __repr__(self):
        return f"<Book id={self.id!r} title={self.title!r} author={self.author!r} borrowings={self.borrowings!r}>"


class User(Base):
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(String(6), primary_key=True)

    borrowings: Mapped[list["Borrowing"]] = relationship(back_populates="user")

    def __repr__(self):
        return f"<User id={self.id!r} borrowings={self.borrowings!r}>"


class Borrowing(Base):
    __tablename__ = "borrowings"

    id: Mapped[int] = mapped_column(primary_key=True)
    start_time: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    end_time: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))

    book_id: Mapped[Optional[str]] = mapped_column(ForeignKey("books.id"))
    user_id: Mapped[Optional[str]] = mapped_column(ForeignKey("users.id"))
    book: Mapped[Optional[Book]] = relationship(back_populates="borrowings")
    user: Mapped[Optional[User]] = relationship(back_populates="borrowings")
