from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi_sqlalchemy import db

from app.auth.auth_bearer import JWTBearer
from app.models.post import Post
from app.models.user import User
from app.schemas.post import PostSchema
from app.schemas.user import UserFullSchema
from utils.dependencies import get_user_from_token

posts_router = APIRouter(
    prefix="/api/v1", dependencies=[Depends(JWTBearer())], tags=["Posts"]
)


@posts_router.get(
    "/posts",
    dependencies=[Depends(JWTBearer())],
    summary="Show all posts",
)
async def get_posts(limit: int = 25, offset: int = 0):
    return db.session.query(Post).limit(limit).offset(offset).all()


@posts_router.post("/posts/create", summary="Add a post")
async def create_post(post: PostSchema, user: Annotated[User, Depends(get_user_from_token)]):
    if user:
        db_post = Post(title=post.title, text=post.text, user_id=user.id)
        db.session.add(db_post)
        db.session.commit()
        return "Post created."
    return 404


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
)
def update_post(
    user: Annotated[UserFullSchema, Depends(get_user_from_token)],
    post_id: int,
    post_update: PostSchema,
):
    existing_post = db.session.get(Post, post_id)
    if existing_post.user != user.id:
        raise HTTPException(status_code=401, detail='Error: only post author can edit it')
    if not existing_post:
        raise HTTPException(status_code=404, detail="Post not found")
    db.session.query(Post).filter(Post.id == post_id).update(post_update.model_dump(exclude_unset=True))
    db.session.commit()
    return f"Post {post_id} successfully edited."


@posts_router.delete(
    "/post/{post_id}",
    summary="Delete a post",
)
async def delete_post(post_id: int):
    db_post = db.session.query(Post).filter_by(id=post_id).one_or_none()
    db.session.delete(db_post)
    db.session.commit()
    return f"Post {post_id} is deleted."
