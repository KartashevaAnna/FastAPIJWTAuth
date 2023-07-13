import bcrypt
from fastapi import APIRouter, Body
from fastapi_sqlalchemy import db

from app.auth.auth_handler import sign_JWT
from app.models import User
from app.schemas.user import UserInSchema, UserLoginSchema, UserOutSchema

auth_router = APIRouter(prefix="/api/v1", tags=["Auth"])

SALT = b"$2b$12$b6HezbZpslamxu5/wv8UU."


@auth_router.post(
    "/user/signup", response_model=UserOutSchema, summary="Add new user"
)
async def user(user: UserInSchema = Body(...)):
    try:
        hashed_password = bcrypt.hashpw(user.password.encode("utf-8"), SALT)
        db_user = User(
            email=user.email,
            password=str(hashed_password),
        )
        db.session.add(db_user)
        db.session.commit()
        return db_user
    except Exception as error:
        return f"This email is already in use. Please, choose another."


def check_user(data: UserLoginSchema):
    user = db.session.query(User).filter_by(email=data.email).one()
    hashed_password = str(bcrypt.hashpw(data.password.encode("utf-8"), SALT))
    if user.email == data.email and user.password == hashed_password:
        return True
    return False


@auth_router.post("/user/login")
async def user_login(user: UserLoginSchema = Body(...)):
    if check_user(user):
        return sign_JWT(user.email)
    return {"error": "Wrong login details!"}
