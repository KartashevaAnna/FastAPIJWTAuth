from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi_sqlalchemy import db

from app.auth.auth_bearer import JWTBearer
from app.models.like import Like
from app.models.post import Post
from app.models.user import User
from app.schemas.like import LikeCreateSchema
from utils.dependencies import get_user_from_token

likes_router = APIRouter(
    prefix="/api/v1", dependencies=[Depends(JWTBearer())], tags=["Likes"]
)


@likes_router.get(
    "/likes",
    dependencies=[Depends(JWTBearer())],
    summary="Show all likes",
)
async def get_likes(limit: int = 25, offset: int = 0):
    return db.session.query(Like).limit(limit).offset(offset).all()


@likes_router.post(
    "/likes/create",
    summary="Create or update a like",
    description="Send a like to create a Like object. The Like object can have 'is_like' set to True or False to "
    "represent likes and dislikes. It can also be set to None. Send the same request to remove your like "
    "(It won't be removed from the database, but its value in 'is_like' field will be reset to None). "
    "Send the request with the opposite value in the field 'is_like' to change like to dislike and vice "
    "versa.",
)
async def create_like(
    like: LikeCreateSchema, user: Annotated[User, Depends(get_user_from_token)]
):
    if user:
        new_like = Like(user_id=user.id, post_id=like.post_id, is_like=like.is_like)
        if db.session.get(Post, new_like.post_id).user == user:
            raise HTTPException(
                status_code=403, detail="You cannot like or dislike your own post."
            )
        else:
            previous_like = (
                db.session.query(Like)
                .filter_by(user_id=user.id, post_id=like.post_id)
                .one_or_none()
            )
            if previous_like:
                if previous_like.is_like != like.is_like:
                    previous_bool = previous_like.is_like
                    db.session.query(Like).filter_by(
                        user_id=user.id,
                        post_id=like.post_id,
                        is_like=previous_like.is_like,
                    ).update(
                        {
                            "user_id": user.id,
                            "post_id": like.post_id,
                            "is_like": like.is_like,
                        }
                    )
                    db.session.commit()
                    return f"{previous_bool} changed to {like.is_like}"
                else:
                    db.session.query(Like).filter_by(
                        user_id=user.id, post_id=like.post_id, is_like=like.is_like
                    ).update(
                        {"user_id": user.id, "post_id": like.post_id, "is_like": None}
                    )
                    db.session.commit()
                    return f"{previous_like.is_like} removed"

            else:
                db.session.add(new_like)
                db.session.commit()
                return "Like created."
    return HTTPException(status_code=404, detail="User not found")


@likes_router.delete(
    "/likes/{like_id}",
    summary="Delete a like",
)
async def delete_like(like_id: int):
    db_like = db.session.query(Like).filter_by(id=like_id).one_or_none()
    db.session.delete(db_like)
    db.session.commit()
    return f"Like {like_id} is deleted."
