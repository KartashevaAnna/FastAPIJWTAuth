from pydantic import BaseModel, Field


class PostSchema(BaseModel):
    title: str = Field(...)
    text: str = Field(...)
    author_id: int

    class Config:
        from_attributes = True
