import uuid
from typing import Optional

_books: dict = {}


def create_book(book_data: dict) -> dict:
    book = {
        "id": str(uuid.uuid4()),
        "title": book_data["title"],
        "author": book_data["author"],
        "status": book_data["status"],
    }
    _books[book["id"]] = book
    return book


def get_all_books() -> list:
    return list(_books.values())


def get_book(book_id: str) -> Optional[dict]:
    return _books.get(book_id)


def update_book_status(book_id: str, status: str) -> Optional[dict]:
    book = _books.get(book_id)
    if book is None:
        return None
    book["status"] = status
    return book


def reset_books() -> None:
    _books.clear()
