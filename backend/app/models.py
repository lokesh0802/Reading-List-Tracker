from pydantic import BaseModel

VALID_STATUSES = ("to-read", "reading", "done")


class Book(BaseModel):
    id: str
    title: str
    author: str
    status: str


class BookCreate(BaseModel):
    title: str
    author: str
    status: str


class BookStatusUpdate(BaseModel):
    status: str
