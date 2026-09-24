import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.storage import reset_books

client = TestClient(app)

@pytest.fixture(autouse=True)
def setup_teardown():
    reset_books()
    yield

def test_valid_add():
    response = client.post("/api/books", json={
        "title": "The Hobbit",
        "author": "J.R.R. Tolkien",
        "status": "to-read"
    })
    assert response.status_code == 201
    data = response.json()
    assert "id" in data
    assert isinstance(data["id"], str)
    assert data["title"] == "The Hobbit"
    assert data["author"] == "J.R.R. Tolkien"
    assert data["status"] == "to-read"

def test_missing_title():
    # Empty title
    res1 = client.post("/api/books", json={"title": "   ", "author": "Author", "status": "to-read"})
    assert res1.status_code == 400
    assert "error" in res1.json()

    # Missing title key entirely
    res2 = client.post("/api/books", json={"author": "Author", "status": "to-read"})
    assert res2.status_code == 400
    assert "error" in res2.json()

def test_invalid_status():
    res = client.post("/api/books", json={"title": "T", "author": "A", "status": "unknown"})
    assert res.status_code == 400
    assert "error" in res.json()

def test_list_includes_added():
    post_res = client.post("/api/books", json={"title": "List Test", "author": "A", "status": "to-read"})
    assert post_res.status_code == 201
    book_id = post_res.json()["id"]

    get_res = client.get("/api/books")
    assert get_res.status_code == 200
    books = get_res.json()
    assert any(b["id"] == book_id and b["title"] == "List Test" for b in books)

def test_status_filter():
    client.post("/api/books", json={"title": "Filter 1", "author": "A", "status": "to-read"})
    client.post("/api/books", json={"title": "Filter 2", "author": "B", "status": "reading"})

    res = client.get("/api/books?status=to-read")
    assert res.status_code == 200
    books = res.json()
    assert len(books) > 0
    assert all(b["status"] == "to-read" for b in books)

def test_stats_returns_counts():
    client.post("/api/books", json={"title": "Stats 1", "author": "A", "status": "to-read"})
    client.post("/api/books", json={"title": "Stats 2", "author": "A", "status": "to-read"})
    
    res = client.get("/api/stats")
    assert res.status_code == 200
    stats = res.json()
    assert stats.get("to-read") == 2
    assert stats.get("reading") == 0
    assert stats.get("done") == 0

def test_patch_changes_status():
    post_res = client.post("/api/books", json={"title": "Patch Test", "author": "A", "status": "to-read"})
    assert post_res.status_code == 201
    book_id = post_res.json()["id"]

    patch_res = client.patch(f"/api/books/{book_id}", json={"status": "reading"})
    assert patch_res.status_code == 200
    data = patch_res.json()
    assert data["status"] == "reading"
    assert data["id"] == book_id
