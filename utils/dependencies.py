from typing import Annotated

from fastapi import Depends, Header
from fastapi_sqlalchemy import db

from app.auth.auth_handler import decode_JWT
from app.models.user import User


def get_token_from_header(authorization: Annotated[str | None, Header()] = None) -> str:
    return authorization.split(" ")[1]


def get_user_name_from_token(token: Annotated[str, Depends(get_token_from_header)]):
    email = decode_JWT(token).get("user_email")
    return db.session.query(User).filter_by(email=email).one_or_none()
