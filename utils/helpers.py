import time

import bcrypt
import jwt
from fastapi_sqlalchemy import db
from pydantic import EmailStr

from app.models.user import User
from app.schemas.token import TokenSchema
from app.schemas.user import UserFullSchema
from config import JWT_ALGORITHM, JWT_SECRET, SALT


def sign_jwt(email: EmailStr) -> str:
    return TokenSchema(email=email).token


def hash_password(password: str) -> str:
    return str(bcrypt.hashpw(password.encode("utf-8"), SALT))


def is_user_in_db(credentials: UserFullSchema):
    hashed_password = hash_password(credentials.password)
    return bool(
        db.session.query(User)
        .filter_by(email=credentials.email, password=hashed_password)
        .one_or_none()
    )


def decode_jwt(token: str) -> dict:
    try:
        decoded_token = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return decoded_token if decoded_token["expires"] >= time.time() else None
    except:
        return {}
