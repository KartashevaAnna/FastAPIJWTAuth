import fastapi
from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder
from fastapi_sqlalchemy import db
from sqlalchemy.exc import IntegrityError

from app.models.user import User
from app.schemas.user import UserFullSchema
from utils.helpers import hash_password, is_user_in_db, sign_jwt
from utils.responses import DUPLICATE_409, ERROR_RESPONSES, UNIVERSAL_200

auth_router = APIRouter(prefix="/api/v1", tags=["Auth"])


@auth_router.post(
    "/user/signup",
    summary="Add new user",
    responses={**UNIVERSAL_200, **ERROR_RESPONSES, **DUPLICATE_409},
)
async def create_user(credentials: UserFullSchema = Body(...)):
    hashed_password = hash_password(credentials.password)
    try:
        db_user = User(
            email=credentials.email,
            password=str(hashed_password),
        )
        db.session.add(db_user)
        db.session.commit()
    except IntegrityError:
        return fastapi.Response(
            status_code=409, content=jsonable_encoder({"detail": "Duplicate values"})
        )
    return "User successfully created."


@auth_router.post(
    "/user/login",
    responses={
        **ERROR_RESPONSES,
    },
)
async def login_user(credentials: UserFullSchema = Body(...)):
    if is_user_in_db(credentials):
        return sign_jwt(credentials.email)
    return {"error": "Wrong login details!"}
