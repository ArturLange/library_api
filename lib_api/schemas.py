from datetime import UTC, datetime

from pydantic import BaseModel, computed_field, field_validator


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
        return numeric_id_check(value)


class User(UserBase):

    class Config:
        from_attributes = True


class UserCreate(UserBase):
    pass


class BorrowingBase(BaseModel):
    start_time: datetime | None = None
    end_time: datetime | None = None
    user_id: str | None = None

    class Config:
        from_attributes = True

    @computed_field
    @property
    def is_active(self) -> bool:
        return self.end_time is None or self.end_time > datetime.now(UTC)


class BorrowingCreate(BorrowingBase):
    user_id: str

    @field_validator("user_id")
    @classmethod
    def user_id_check(cls, value: str) -> str:
        return numeric_id_check(value)


class BookWithBorrowings(Book):
    borrowings: list[BorrowingBase]

    @computed_field
    @property
    def is_currently_borrowed(self) -> bool:
        return any(borrowing.is_active for borrowing in self.borrowings)


class BookReturn(BaseModel):
    end_time: datetime | None = None
