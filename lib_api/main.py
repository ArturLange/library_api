from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session

from lib_api import crud, schemas
from lib_api.db import get_db

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello, World!"}


@app.get("/books", response_model=list[schemas.Book])
async def get_books(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_books(db, skip=skip, limit=limit)


@app.post("/books")
async def add_book(book: schemas.BookCreate, db: Session = Depends(get_db)):
    return crud.create_book(db=db, book=book)
