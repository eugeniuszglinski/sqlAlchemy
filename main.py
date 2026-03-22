from typing import Annotated

from fastapi import FastAPI, Depends

from pydantic import BaseModel, Field
from sqlalchemy import select
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

import uvicorn


app = FastAPI()


engine = create_async_engine('sqlite+aiosqlite:///books.db')

# this is a way to create the table without using the ORM, but I will use the ORM to create the table and perform CRUD operations.
# with engine.connect() as conn:
#     conn.execute('CREATE TABLE IF NOT EXISTS books (id INTEGER PRIMARY KEY, title TEXT, author TEXT)')

new_session = async_sessionmaker(engine, expire_on_commit=False)


# this is a dependency generator that will be used in the endpoints to get a session.
# it will create a new session for each request and close it after the request is done.
async def get_session():
    async with new_session() as session:
        yield session


SessionDependency = Annotated[AsyncSession, Depends(get_session)]


class Base(DeclarativeBase):
    pass


class BookModel(Base):
    __tablename__ = 'books'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column()
    author: Mapped[str] = mapped_column()


class BookAddSchema(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    author: str = Field(..., min_length=1, max_length=100)


class BookSchema(BookAddSchema):
    id: int = Field(...)


@app.post("/create_tables")
async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    return {"message": "Tables created successfully"}


@app.post("/books")
async def add_book(data: BookAddSchema, session: SessionDependency):
    new_book = BookModel(title=data.title, author=data.author)
    session.add(new_book)
    await session.commit()
    await session.refresh(new_book)
    return {"message": "Book added successfully"}


@app.delete("/books/{book_id}")
async def delete_book(book_id: int, session: SessionDependency):
    book = await session.get(BookModel, book_id)
    if not book:
        return {"message": "Book not found"}
    await session.delete(book)
    await session.commit()
    return {"message": "Book deleted successfully"}


@app.put("/books/{book_id}")
async def update_book(book_id: int, data: BookAddSchema, session: SessionDependency):
    book = await session.get(BookModel, book_id)
    if not book:
        return {"message": "Book not found"}
    book.title = data.title
    book.author = data.author
    await session.commit()
    await session.refresh(book)
    return {"message": "Book updated successfully"}


@app.get("/books/{book_id}")
async def get_book(book_id: int, session: SessionDependency):
    book = await session.get(BookModel, book_id)
    if not book:
        return {"message": "Book not found"}
    return book


@app.get("/books")
async def get_books(session: SessionDependency):
    books = await session.execute(select(BookModel))
    return books.scalars().all()


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
