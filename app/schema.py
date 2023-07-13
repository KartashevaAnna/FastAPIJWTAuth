from pydantic import BaseModel, EmailStr, Field


class PostSchema(BaseModel):
    title: str = Field(...)
    content: str = Field(...)
    author_id: int

    class Config:
        from_attributes = True
