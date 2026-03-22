from pydantic import BaseModel, Field


class BookAddSchema(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    author: str = Field(..., min_length=1, max_length=100)


class BookSchema(BookAddSchema):
    id: int = Field(...)
