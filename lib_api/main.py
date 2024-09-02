from fastapi import Depends, FastAPI
from lib_api.db import get_db
from lib_api.models import Book
from sqlalchemy.orm import Session

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello, World!"}


@app.get("/books")
async def get_books(db: Session = Depends(get_db)):
    return db.query(Book).all()
