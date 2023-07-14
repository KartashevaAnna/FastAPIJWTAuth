from typing import Annotated

from fastapi import Depends, Header
from fastapi_sqlalchemy import db

from app.models.user import User
from utils.helpers import decode_token


def get_token_from_header(authorization: Annotated[str | None, Header()] = None) -> str:
    return authorization.split(" ")[1]


def get_user_from_token(token: Annotated[str, Depends(get_token_from_header)]) -> User | None:
    email = decode_token(token).get("email")
    return db.session.query(User).filter_by(email=email).one_or_none()
