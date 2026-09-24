from fastapi import APIRouter
from fastapi.responses import JSONResponse

from app.models import VALID_STATUSES
from app.storage import get_all_books

router = APIRouter()


@router.get("/api/books")
def list_books(status: str | None = None):
    if status is not None and status not in VALID_STATUSES:
        return JSONResponse(status_code=400, content={"error": "invalid status"})

    books = get_all_books()
    if status is None:
        return books
    return [book for book in books if book["status"] == status]


@router.get("/api/stats")
def get_stats():
    counts = {status: 0 for status in VALID_STATUSES}
    for book in get_all_books():
        counts[book["status"]] += 1
    return counts
