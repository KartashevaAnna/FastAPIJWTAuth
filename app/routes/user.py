from fastapi import APIRouter
from fastapi_sqlalchemy import db

from app.models import User

users_router = APIRouter(prefix="/api/v1", tags=["Users"])


@users_router.get("/user/", summary="Show all users")
async def user():
    users = db.session.query(User).all()
    return users


@users_router.post("/users/", summary="Delete all users")
async def user():
    users = db.session.query(User).all()
    for user in users:
        db.session.delete(user)
    db.session.commit()
    return 200
