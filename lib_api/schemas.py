from pydantic import BaseModel


class BookBase(BaseModel):
    id: str
    title: str
    author: str


class Book(BookBase):

    class Config:
        from_attributes = True


class BookCreate(BookBase):
    pass
