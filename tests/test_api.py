import pytest

from httpx import AsyncClient, ASGITransport
from main import app


@pytest.mark.asyncio
async def test_create_tables():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.post("/create_tables")
    assert response.status_code == 200
    assert response.json() == {"message": "Tables created successfully"}


@pytest.mark.asyncio
async def test_add_book():
    book_data = {"title": "The Great Gatsby", "author": "F. Scott Fitzgerald"}

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.post("/books", json=book_data)
    assert response.status_code == 200
    assert response.json() == {"message": "Book added successfully"}


@pytest.mark.asyncio
async def test_get_books():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get("/books")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) == 1
    assert response.json()[0]["title"] == "The Great Gatsby"
    assert response.json()[0]["author"] == "F. Scott Fitzgerald"


@pytest.mark.asyncio
async def test_update_book():
    updated_data = {"title": "The Great Gatsby Updated", "author": "F. Scott Fitzgerald"}

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.put("/books/1", json=updated_data)
    assert response.status_code == 200
    assert response.json() == {"message": "Book updated successfully"}


@pytest.mark.asyncio
async def test_get_book():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get("/books/1")
    assert response.status_code == 200
    assert response.json()["title"] == "The Great Gatsby Updated"
    assert response.json()["author"] == "F. Scott Fitzgerald"


@pytest.mark.asyncio
async def test_delete_book():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.delete("/books/1")
    assert response.status_code == 200
    assert response.json() == {"message": "Book deleted successfully"}

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get("/books/1")
    assert response.status_code == 200
    assert response.json() == {"message": "Book not found"}
