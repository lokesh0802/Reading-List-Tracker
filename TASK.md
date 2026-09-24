# TASKS.md — single-run live board (main only)

All work is on branch main. No task branches. Each row owns files, not a branch.

## Five parallel tasks
[ ] T1 — Write API: create + update status | Claude Code #1 (Sonnet 5) | models.py, storage.py, routers/books_write.py
[ ] T2 — Read API: list + filter + stats | Cursor chat A (Auto) | routers/books_read.py
[ ] T3 — UI: add / view / change status | Cursor chat B (Auto) | index.html, app.js, styles.css
[ ] T4 — Core API tests | Gemini (Gemini 3.1 Pro) | tests/test_books.py
[ ] T5 — App wiring + deployment files | Claude Code #2 (Sonnet 5) | main.py, requirements.txt, render.yaml, config.js, vercel.json

## One sequential step (only after T1–T5 have commits, and only after the 404 is on screen)
[ ] INT — Mount the two routers in main.py, re-run pytest, push, set URLs, live demo

Legend: [ ] not started | [~] running | [R] ready for review | [x] reviewed and committed on main

Coordinator rule: one owner, one file set per row. Update this board when a session starts, when it returns for review, and when its files are committed. No agent edits this file. No second round. No extra tasks.