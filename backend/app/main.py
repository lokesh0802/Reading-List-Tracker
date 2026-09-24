import os
import sys

if __package__ in (None, ""):
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.routers import books_read, books_write

VERCEL_ORIGIN = "https://reading-list-tracker.vercel.app"

DEFAULT_CORS_ORIGINS = (
    "http://localhost:3000,http://localhost:5500,http://127.0.0.1:5500,"
    "http://127.0.0.1:8000,http://[::1]:5500,http://[::]:5500,"
    + VERCEL_ORIGIN
)

app = FastAPI(title="Reading List Tracker")

origins = [
    origin.strip().rstrip("/")
    for origin in os.environ.get("CORS_ORIGINS", DEFAULT_CORS_ORIGINS).split(",")
    if origin.strip()
]
if VERCEL_ORIGIN not in origins:
    origins.append(VERCEL_ORIGIN)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(status_code=400, content={"error": str(exc)})


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    return JSONResponse(status_code=exc.status_code, content={"error": exc.detail})


app.include_router(books_write.router)
app.include_router(books_read.router)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
