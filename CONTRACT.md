# CONTRACT.md — Reading List Tracker

## Repository and deployment
- One branch only: main. No task branches, no worktrees, no merges.
- backend/: FastAPI/Python 3.11 API, deployed on Render. Render root is backend/.
- frontend/: static HTML/CSS/JavaScript, deployed on Vercel. Vercel root is frontend/.
- The services have different public URLs. Do not assume a shared domain.
- Storage is one in-memory list for this exercise.
- Frontend requests must use API_BASE_URL from frontend/config.js.
- Backend CORS allowed origins come from comma-separated CORS_ORIGINS.

## Book model
- id: server-generated UUID string.
- title: required, non-empty after trimming whitespace.
- author: required, non-empty after trimming whitespace.
- status: exactly to-read, reading, or done.
- No uniqueness rule for title.

## API contract
- POST /api/books — body {title, author, status}; returns 201 and the created book.
- Missing/blank title or author, or an invalid status, returns 400 with {"error":"<message>"}.
- GET /api/books — returns all books.
- GET /api/books?status=to-read|reading|done — returns only matching books.
- Invalid status query returns 400 with {"error":"<message>"}.
- GET /api/stats — returns all three counts, e.g. {"to-read": 2, "reading": 1, "done": 0}.
- PATCH /api/books/{id} — body {status}; returns 200 and the updated book.
- PATCH with an invalid status returns 400 with {"error":"<message>"}.
- PATCH for an unknown ID returns 404 with {"error":"<message>"}.

## Shared storage interface
T1 implements these helpers in backend/app/storage.py. T2 imports them
and must not create a second store:
- create_book(book_data) -> book
- get_all_books() -> list[book]
- get_book(book_id) -> book or None
- update_book_status(book_id, status) -> book or None
- reset_books() -> None (test helper)

T1 also defines VALID_STATUSES in backend/app/models.py so T2 can import it.

## File ownership — each task edits only its own files, all on main
- T1: backend/app/models.py, backend/app/storage.py, backend/app/routers/books_write.py
- T2: backend/app/routers/books_read.py only
- T3: frontend/index.html, frontend/app.js, frontend/styles.css
- T4: backend/tests/test_books.py only
- T5: backend/app/main.py, backend/requirements.txt, render.yaml, frontend/config.js, frontend/vercel.json
- During the parallel pass, T5 must not import or include books_write or books_read.
  Mounting those routers is the later integration step, in main.py only.
- After deploy, the only config hand-off is the API URL value in frontend/config.js
  and Render's CORS_ORIGINS value.
- CONTRACT.md and TASKS.md are coordinator-owned. Agents read them and do not edit them.

## Rules
1. Follow this contract. Do not add routes, fields, statuses, or features.
2. Preserve the error shape and status codes above. Use 400, not FastAPI's default 422.
3. T1 and T2 use the same storage helpers. T2 does not edit T1's files.
4. T3 imports API_BASE_URL from ./config.js. It does not hardcode a backend host and it does not edit config.js.
5. Stay on main. Edit only your owned files. Stage only those paths. Do not create a branch. Do not run git add . or git add -A.
6. Do not weaken or delete a test just to make the suite pass.

API shape used by all agents:
{"id": "a-server-generated-uuid", "title": "The Left Hand of Darkness", "author": "Ursula K. Le Guin", "status": "to-read"}

GET /api/stats always includes all three keys, including zero counts.


## Folder strucutre
reading-list-tracker/
  CONTRACT.md                 
  TASKS.md                    
  README.md                   
  render.yaml                 T5
  backend/
    requirements.txt          T5
    app/
      __init__.py             
      main.py                 starter shell before recording; T5 edits it; INT mounts routers
      models.py               T1
      storage.py              T1
      routers/
        __init__.py           
        books_write.py        T1
        books_read.py         T2
    tests/
      test_books.py           T4
  frontend/
    index.html                T3
    app.js                    T3
    styles.css                T3
    config.js                 
    vercel.json               T5