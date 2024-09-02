from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from lib_api import crud, schemas
from lib_api.db import get_db

router = APIRouter()


@router.get("/", response_model=list[schemas.BookWithBorrowings])
async def get_books(
    skip: int | None = None, limit: int | None = None, db: Session = Depends(get_db)
):
    db_books = crud.get_books(db, skip=skip, limit=limit)
    return db_books


@router.post(
    "/", response_model=schemas.BookWithBorrowings, status_code=status.HTTP_201_CREATED
)
async def add_book(book: schemas.BookCreate, db: Session = Depends(get_db)):
    db_book = crud.get_book_with_details(db, book_id=book.id)
    if db_book:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Book with given id already exists",
        )
    return crud.create_book(db=db, book=book)


@router.get("/{book_id}", response_model=schemas.BookWithBorrowings)
async def get_book(book_id: str, db: Session = Depends(get_db)):
    db_book = crud.get_book_by_id(db, book_id=book_id)
    if not db_book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Book not found"
        )
    return db_book


@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: str, db: Session = Depends(get_db)):
    crud.delete_book(db, book_id=book_id)

    return Response(status_code=204)


@router.post(
    "/{book_id}/borrow",
    response_model=schemas.Book,
    status_code=status.HTTP_201_CREATED,
)
async def borrow_book(
    book_id: str, borrowing_data: schemas.BorrowingCreate, db: Session = Depends(get_db)
):
    db_book, _ = crud.create_borrowing(db, borrowing_data, book_id)

    return db_book


@router.post(
    "/{book_id}/return",
    response_model=schemas.Book,
    status_code=status.HTTP_201_CREATED,
)
async def return_book(
    book_id: str, return_data: schemas.BookReturn, db: Session = Depends(get_db)
):
    db_borrowing = crud.get_borrowing(db, book_id)
    if return_data.end_time:
        db_borrowing.end_time = return_data.end_time
    db.add(db_borrowing)
    db.commit()
    db.refresh(db_borrowing)
    return db_borrowing.book
