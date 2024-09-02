from sqlalchemy.orm import Session

from lib_api import models, schemas

# BOOKS


def get_books(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Book).offset(skip).limit(limit).all()


def create_book(db: Session, book: schemas.BookCreate) -> models.Book:
    db_book = models.Book(**book.model_dump())
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book


def get_book_by_id(db: Session, book_id: str):
    return db.query(models.Book).filter(models.Book.id == book_id).first()


def delete_book(db: Session, book_id: str) -> None:
    db_book = get_book_by_id(db, book_id)
    db.delete(db_book)
    db.commit()


# USERS


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate) -> models.User:
    db_user = models.User(**user.model_dump())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user_by_id(db: Session, user_id: str):
    return db.query(models.User).filter(models.User.id == user_id).first()


def delete_user(db: Session, user_id: str) -> None:
    db_user = get_user_by_id(db, user_id)
    db.delete(db_user)
    db.commit()


# BORROWINGS


def create_borrowing(
    db: Session, borrowing: schemas.BorrowingBase, book_id: str
) -> models.Borrowing:
    db_borrowing = models.Borrowing(**borrowing.model_dump())
    db_user = get_user_by_id(db, borrowing.user_id)
    db_book = get_book_by_id(db, book_id)
    db_borrowing.user = db_user
    db_borrowing.book = db_book
    db.add(db_borrowing)
    db.commit()
    db.refresh(db_book)
    db.refresh(db_borrowing)
    return db_book, db_borrowing


def get_borrowing(db: Session, book_id: str):
    return (
        db.query(models.Borrowing)
        .filter(models.Borrowing.end_time == None)
        .filter(models.Borrowing.book_id == book_id)
        .first()
    )
