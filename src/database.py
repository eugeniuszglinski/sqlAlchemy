from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase


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


class Base(DeclarativeBase):
    pass
