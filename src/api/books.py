from fastapi import APIRouter
from sqlalchemy import select

from src.api.dependencies import SessionDependency
from src.database import engine, Base
from src.models.books import BookModel
from src.schemas.books import BookAddSchema


router = APIRouter(prefix="/books", tags=["Books"])


@router.post("/create_tables")
async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    return {"message": "Tables created successfully"}


@router.post("/books")
async def add_book(data: BookAddSchema, session: SessionDependency):
    new_book = BookModel(title=data.title, author=data.author)
    session.add(new_book)
    await session.commit()
    await session.refresh(new_book)
    return {"message": "Book added successfully"}


@router.delete("/books/{book_id}")
async def delete_book(book_id: int, session: SessionDependency):
    book = await session.get(BookModel, book_id)
    if not book:
        return {"message": "Book not found"}
    await session.delete(book)
    await session.commit()
    return {"message": "Book deleted successfully"}


@router.put("/books/{book_id}")
async def update_book(book_id: int, data: BookAddSchema, session: SessionDependency):
    book = await session.get(BookModel, book_id)
    if not book:
        return {"message": "Book not found"}
    book.title = data.title
    book.author = data.author
    await session.commit()
    await session.refresh(book)
    return {"message": "Book updated successfully"}


@router.get("/books/{book_id}")
async def get_book(book_id: int, session: SessionDependency):
    book = await session.get(BookModel, book_id)
    if not book:
        return {"message": "Book not found"}
    return book


@router.get("/books")
async def get_books(session: SessionDependency):
    books = await session.execute(select(BookModel))
    return books.scalars().all()
