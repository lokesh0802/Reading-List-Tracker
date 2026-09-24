# Reading List Tracker

A small full-stack app for tracking books you want to read, are reading, or have finished.

- **Backend**: FastAPI + Python 3.11, in-memory storage (no database — data resets on restart).
- **Frontend**: Static HTML/CSS/vanilla JavaScript, no build step, no framework.

## Project structure

```
reading-list-tracker/
  backend/
    app/
      main.py              # FastAPI app: CORS, error handlers, router mounting
      models.py            # Book/BookCreate/BookStatusUpdate models + VALID_STATUSES
      storage.py           # In-memory data store (single dict, shared by both routers)
      routers/
        books_write.py     # POST /api/books, PATCH /api/books/{id}
        books_read.py      # GET /api/books, GET /api/stats
    tests/
      test_books.py        # pytest + FastAPI TestClient integration tests
    requirements.txt
  frontend/
    index.html              # Page markup (add-book form, stats, book list)
    app.js                  # Fetch calls to the API, rendering, event handlers
    styles.css
    config.js                # API_BASE_URL — the one place the frontend points at a backend
    vercel.json
  render.yaml                # Render deployment config for the backend
  CONTRACT.md                 # API/behavior contract this app was built against
```

## How the pieces connect

- `frontend/app.js` imports `API_BASE_URL` from `frontend/config.js` and calls the backend
  only through that URL — never hardcoded elsewhere.
- `backend/app/main.py` mounts both routers (`books_write`, `books_read`) and defines shared
  CORS + error handling. **Both routers must be mounted here for any `/api/*` route to work.**
- `backend/app/routers/books_write.py` and `books_read.py` both import their storage helpers
  from `backend/app/storage.py` — there is exactly one in-memory store, shared by both routers.
- `backend/app/models.py` defines `VALID_STATUSES = ("to-read", "reading", "done")`, imported
  by both routers so status validation stays consistent.

## Prerequisites

- Python 3.11
- A modern browser (frontend needs no build tooling)

## Running locally

### 1. Backend

```bash
cd backend
python3.11 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python3 app/main.py
```

(equivalent to `uvicorn app.main:app --reload --port 8000`, run either way)

The API is now at `http://127.0.0.1:8000`. Quick check:

```bash
curl http://127.0.0.1:8000/api/books
```

### 2. Frontend

`frontend/config.js` already points at `http://127.0.0.1:8000` for local dev. Serve the
frontend as static files (it uses ES module `<script type="module">`, which most browsers
block on `file://`, so use a local server):

```bash
cd frontend
python3 -m http.server 5500
```

Open `http://127.0.0.1:5500` in your browser.

### 3. Run the tests

```bash
cd backend
source .venv/bin/activate
python -m pytest tests -q
```

## API reference

| Method | Path                     | Body                          | Notes |
|--------|--------------------------|--------------------------------|-------|
| POST   | `/api/books`             | `{title, author, status}`      | 201 + created book. 400 on blank title/author or invalid status. |
| GET    | `/api/books`             | —                               | All books. |
| GET    | `/api/books?status=X`    | —                               | Filtered by status. 400 if `X` is invalid. |
| GET    | `/api/stats`             | —                               | `{"to-read": n, "reading": n, "done": n}`, always all three keys. |
| PATCH  | `/api/books/{id}`        | `{status}`                     | 200 + updated book. 400 invalid status, 404 unknown id. |

Book shape: `{"id": "<uuid>", "title": "...", "author": "...", "status": "to-read"}`.
Errors are always `{"error": "<message>"}`.

Full contract: see [CONTRACT.md](CONTRACT.md).

## Deployment

- **Backend → Render**: root directory `backend/`, config in [render.yaml](render.yaml).
  Set the `CORS_ORIGINS` environment variable to a comma-separated list including your
  deployed frontend origin (e.g. `https://your-app.vercel.app`).
- **Frontend → Vercel**: root directory `frontend/`, config in
  [frontend/vercel.json](frontend/vercel.json). No build step.
- After both are deployed, update `frontend/config.js`'s `API_BASE_URL` to the live
  Render URL and redeploy the frontend. The backend and frontend live on different
  domains — there is no shared domain assumption.

## Known limitations

- Storage is a single in-memory dict — all data is lost when the backend process restarts,
  and it is not safe for multiple server instances/workers (no shared persistence).
- No authentication — anyone with the API URL can read/write the list.
