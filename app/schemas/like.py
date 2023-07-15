from pydantic import BaseModel, Field


class LikeCreateSchema(BaseModel):
    post_id: int
    is_like: bool | None

    class Config:
        from_attributes = True


class LikeSchema(LikeCreateSchema):
    user_id: int

    class Config:
        from_attributes = True

