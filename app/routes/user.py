from fastapi import APIRouter
from fastapi_sqlalchemy import db

from app.models.post import Post
from app.models.user import User

users_router = APIRouter(prefix="/api/v1", tags=["Users"])


@users_router.get("/users", summary="Show all users")
async def show_all_users():
    return db.session.query(User).all()


@users_router.post("/clear-database", summary="Delete all posts and all users")
async def delete_all_users():
    db.session.query(Post).delete()
    db.session.query(User).delete()
    db.session.commit()
    return 200
