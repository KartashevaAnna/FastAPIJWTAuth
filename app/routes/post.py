from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi_sqlalchemy import db

from app.auth.auth_bearer import JWTBearer
from app.models.post import Post
from app.schemas.post import PostSchema
from app.schemas.user import UserOutSchema
from utils.dependencies import get_user_name_from_token

posts_router = APIRouter(
    prefix="/api/v1", dependencies=[Depends(JWTBearer())], tags=["Posts"]
)


@posts_router.get(
    "/posts",
    dependencies=[Depends(JWTBearer())],
    summary="Show all posts",
)
async def get_posts():
    posts = db.session.query(Post).all()
    return posts


@posts_router.post("/post", summary="Add a post", status_code=201)
async def add_post(post: PostSchema):
    db_post = Post(title=post.title, text=post.text, user_id=post.user_id)
    db.session.add(db_post)
    db.session.commit()
    return "Post created."


@posts_router.get(
    "/post/{post_id}",
    summary="Show a post",
    response_model=PostSchema,
)
def show_post(post_id: int):
    db_post = db.session.query(Post).filter_by(id=post_id).one_or_none()
    if not db_post:
        raise HTTPException(status_code=404, detail="Post not found")
    return db_post


@posts_router.patch(
    "/post/{post_id}",
    summary="Update a post",
    status_code=200,
)
def update_post(
    user: Annotated[UserOutSchema, Depends(get_user_name_from_token)],
    post_id: int,
    post_to_change: PostSchema,
):
    db_post = db.session.get(Post, post_id)
    if not db_post:
        raise HTTPException(status_code=404, detail="Post not found")
    post_data = post_to_change.model_dump(exclude_unset=True)
    for key, value in post_data.items():
        setattr(db_post, key, value)
    db.session.add(db_post)
    db.session.commit()
    db.session.refresh(db_post)
    return f"Post {post_id} successfully edited."


@posts_router.delete(
    "/post/{post_id}",
    summary="Delete a post",
    status_code=201,
)
async def remove_post(post_id):
    db_post = db.session.query(Post).filter_by(id=post_id).one_or_none()
    db.session.delete(db_post)
    db.session.commit()
    return f"Post {post_id} is deleted."
