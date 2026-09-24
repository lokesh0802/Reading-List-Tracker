from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse

from app.models import VALID_STATUSES
from app.storage import create_book as storage_create_book
from app.storage import update_book_status

router = APIRouter()


@router.post("/api/books", status_code=201)
async def create_book(request: Request):
    body = await request.json()
    title = str(body.get("title") or "").strip()
    author = str(body.get("author") or "").strip()
    status = body.get("status")

    if not title:
        return JSONResponse(status_code=400, content={"error": "title is required"})
    if not author:
        return JSONResponse(status_code=400, content={"error": "author is required"})
    if status not in VALID_STATUSES:
        return JSONResponse(status_code=400, content={"error": "invalid status"})

    book = storage_create_book({"title": title, "author": author, "status": status})
    return book


@router.patch("/api/books/{book_id}")
async def patch_book_status(book_id: str, request: Request):
    body = await request.json()
    status = body.get("status")

    if status not in VALID_STATUSES:
        return JSONResponse(status_code=400, content={"error": "invalid status"})

    book = update_book_status(book_id, status)
    if book is None:
        return JSONResponse(status_code=404, content={"error": "book not found"})

    return book
