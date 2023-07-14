from typing import Annotated

from fastapi import Depends, Header
from fastapi_sqlalchemy import db

from app.models.user import User
from utils.helpers import decode_jwt


def get_token_from_header(authorization: Annotated[str | None, Header()] = None) -> str:
    return authorization.split(" ")[1]


def get_user_name_from_token(token: Annotated[str, Depends(get_token_from_header)]):
    email = decode_jwt(token).get("user_email")
    return db.session.query(User).filter_by(email=email).one_or_none()
