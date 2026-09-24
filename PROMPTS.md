## T1-Write API(claude code)
Repo: reading-list-tracker. Branch: main. Do not create a branch.
Read CONTRACT.md and TASKS.md first. You own T1. Confirm the T1 row
lists Claude Code and these files. Stop if another session owns it or
it is already complete.

Implment only:
- backend/app/models.py:Pydantic boook models and VALID_STATUSES exactly as in the contract.
- backend/app/storage.py:one in-mempory store with creat_book.
- backend/app/routers/book_write.py : APIROUTER with POST /api/books and PATCH /api/books/{id}

POST retuns 201, genertaes a UUID , trims ttille authore and rejects missing/blank title or author and invalid status with 400 and {"erro":""} .PATCH changes status only , returns 200 , return 404 for an unknown id , and rejects an invlaid status with 400 and  {"erro":""} . DO not rely on FASTAPI default 422.

Do not implement getouts. Do not edit main.py, books_read.py,
frontend files, tests, CONTRACT.md, or TASKS.md. Do not git add unrealted files .Commit only your three files on main if i ask you to commit. 
REport files changed , behaviour and any assumption in plain text.
## T2 — Read API (Cursor chat A, Auto)
Repo: reading-list-tracker. Branch: main. Do not create a branch.
Read CONTRACT.md and TASKS.md first. You own T2. Confirm the T2 row
is this Cursor chat and backend/app/routers/books_read.py only. Stop
if another session owns it or it is complete.
Implement only backend/app/routers/books_read.py:
1. GET /api/books, all books, optional ?status=to-read|reading|done.
2. GET /api/stats, counts for all three statuses, including zeroes.

Import get_all_books from backend/app/storage.py and VALID_STATUSES from
backend/app/models.py.
Do not create a second store.
Do not edit T1's
files. Invalid status returns 400 and {"error":"..."}.
 Do not edit
main.py, tests, frontend, deployment files, CONTRACT.md, or TASKS.md.
Do not git add unrelated files. Report exactly what changed.

## T3- UI(crusor)
Repo: reading-list-tracker. Branch: main. Do not create a branch.
Read CONTRACT.md and TASKS.md first. You own T3. Confirm the T3 row
is this Cursor chat and frontend/index.html, frontend/app.js,
frontend/styles.css. Stop if another session owns it or it is complete.

Build a single page with vanilla HTML CSS and JS .Edit only those three files.
- ADD-book form : title. , author and status(to-read, reading m, done).
- Book list,, a satus filter and count-by-status.
- Each row can change status via PATCH, then refresh the list and stats.
- Use the exact API paths and JSON shapes in CONTRACT.md.
- In app.js, import API_BASE_URL from ./config.js and build every URL
  from it. Do not hardcode a host. Do not create or edit config.js.
- Show a clear success message, and show the API's error message on
  failure, including a blank title.
- No build tool, framework, or extra feature.

Do not edit backend code , tests , depoloyment files , CONTRACT.md and task.md . Reportfiles changed and any assunptions.
## T4 - Tests (Gemini, Gemini 3.1 Pro)
Repo: reading-list-tracker. Branch: main. Do not create a branch.
Read CONTRACT.md and TASKS.md first. You own T4. Confirm the T4 row
is Gemini and backend/tests/test_books.py only. Stop if another session
owns it or it is complete.

Write only backend/tests/test_books.py using FastAPI TestClient against
app.main:app. Cover:
- valid add (201, returned UUID and book)
- missing title (400, error key)
- invalid status (400, error key)
- list includes an added book
- status filter returns only matches
- stats returns correct counts for all three statuses, including zeroes
- PATCH changes status

Use unique titles or count deltas so tests do not depend on leftover
in-memory state. Call reset_books if that helper exists.

do not edit application code. Do not waken or delete an assertion to match a wrong respone.
Run pytest and show the real output. do try to change the existing code which is wriiten in main.py and the routers folder
Commit only backend/tests/test_books.py oif i ask you to commit , Report the failing assertion and the output.



## T5- Deploy and CORS
Repo: reading-list-tracker. Branch: main. Do not create a branch.
Read CONTRACT.md and TASKS.md first. You own T5. Confirm the T5 row
lists Claude Code session two and these files only. Stop if another
session owns it or it is complete.

Own only: backend/app/main.py, backend/requirements.txt, render.yaml,
frontend/config.js, frontend/vercel.json.

- main.py: create the FastAPI app, add CORS middleware reading
  CORS_ORIGINS (comma-separated env var), default
  http://localhost:3000,http://localhost:5500,http://127.0.0.1:8000.
  Normalize request-validation errors to HTTP 400 and {"error":"..."}.
  Normalize other API errors to the same shape.
- Do NOT import books_write or books_read. Do NOT call include_router.
  Those modules are being written by other sessions. I will ask you to
  mount them later, after the tests have shown 404. Leave a short comment
  that the router include is waiting for the integration step.
- requirements.txt: FastAPI, Uvicorn, pytest, httpx. Note Python 3.11.
- render.yaml: Render Python web service, root directory backend/,
  install pip install -r requirements.txt, start
  uvicorn app.main:app --host 0.0.0.0 --port $PORT.
- frontend/config.js: keep a localhost API_BASE_URL placeholder.
- frontend/vercel.json: minimal static-site config.

Do not edit the route modules, tests, index.html, app.js, styles.css,
CONTRACT.md, or TASKS.md. Do not create duplicate router stubs.
Report files changed and any Render or Vercel setting I must click manually.