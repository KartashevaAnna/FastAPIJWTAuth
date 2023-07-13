from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi_sqlalchemy import db

from app.auth.auth_bearer import JWTBearer
from app.dependencies import get_user_name_from_token
from app.models import Post
from app.schemas.post import PostSchema
from app.schemas.user import UserOutSchema

posts_router = APIRouter(
    prefix="/api/v1", dependencies=[Depends(JWTBearer())], tags=["Posts"]
)


@posts_router.get(
    "/posts",
    dependencies=[Depends(JWTBearer())],
    summary="Show all posts",
)
async def get_posts(user: Annotated[UserOutSchema, Depends(get_user_name_from_token)]):
    posts = db.session.query(Post).all()
    return posts


@posts_router.post(
    "/post",
    response_model=PostSchema,
    summary="Add a post",
)
async def add_post(post: PostSchema) -> dict:
    db_post = Post(title=post.title, text=post.text, user_id=post.user_id)
    db.session.add(db_post)
    db.session.commit()
    return db_post


@posts_router.get(
    "/post/{post_id}",
    summary="Show a post",
)
def show_post(post_id: int):
    db_post = db.session.query(Post).filter_by(id=post_id).one_or_none()
    if not db_post:
        raise HTTPException(status_code=404, detail="Post not found")
    return db_post


@posts_router.patch(
    "/post/{post_id}",
    response_model=PostSchema,
    summary="Update a post",
)
def update_post(post_id: int, post_to_change: PostSchema):
    db_post = db.session.get(Post, post_id)
    if not db_post:
        raise HTTPException(status_code=404, detail="Post not found")
    post_data = post_to_change.model_dump(exclude_unset=True)
    for key, value in post_data.items():
        setattr(db_post, key, value)
    db.session.add(db_post)
    db.session.commit()
    db.session.refresh(db_post)
    return db_post


@posts_router.delete(
    "/post/{post_id}",
    summary="Delete a post",
)
async def remove_post(post_id):
    db_post = db.session.query(Post).filter_by(id=post_id).one_or_none()
    db.session.delete(db_post)
    db.session.commit()
    return 200
