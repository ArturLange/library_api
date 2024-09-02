from pydantic import BaseModel, field_validator


def numeric_id_check(value: str) -> str:
    if len(value) != 6 or not set(value) <= set("0123456789"):
        raise ValueError("ID must be a six digit number")
    return value


class BookBase(BaseModel):
    id: str
    title: str
    author: str

    @field_validator("id")
    @classmethod
    def id_check(cls, value: str) -> str:
        return numeric_id_check(value)


class Book(BookBase):

    class Config:
        from_attributes = True


class BookCreate(BookBase):
    pass


class UserBase(BaseModel):
    id: str

    @field_validator("id")
    @classmethod
    def id_check(cls, value: str) -> str:
        numeric_id_check(value)


class User(UserBase):

    class Config:
        from_attributes = True


class UserCreate(UserBase):
    pass
