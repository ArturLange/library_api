from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from lib_api import crud, schemas
from lib_api.db import get_db

router = APIRouter()


@router.get("/", response_model=list[schemas.Book])
async def get_books(
    skip: int | None = None, limit: int | None = None, db: Session = Depends(get_db)
):
    return crud.get_books(db, skip=skip, limit=limit)


@router.post("/", response_model=schemas.Book, status_code=status.HTTP_201_CREATED)
async def add_book(book: schemas.BookCreate, db: Session = Depends(get_db)):
    db_book = crud.get_book_by_id(db, book_id=book.id)
    if db_book:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Book with given id already exists",
        )
    return crud.create_book(db=db, book=book)


@router.get("/{book_id}", response_model=schemas.Book)
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
