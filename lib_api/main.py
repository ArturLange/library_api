from fastapi import FastAPI

from lib_api.routers import books, users

app = FastAPI()

app.include_router(books.router, tags=["books"], prefix="/books")
app.include_router(users.router, tags=["users"], prefix="/users")
