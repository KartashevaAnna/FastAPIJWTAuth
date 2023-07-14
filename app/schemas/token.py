import datetime

import jwt
from pydantic import BaseModel, EmailStr, computed_field

from config import JWT_ALGORITHM, JWT_SECRET, TOKEN_LIFETIME


class TokenPayloadSchema(BaseModel):
    email: EmailStr

    @computed_field
    @property
    def token_expiry(self) -> str:
        return (
            datetime.datetime.utcnow() + datetime.timedelta(hours=TOKEN_LIFETIME)
        ).strftime('%Y-%m-%d %H:%M:%S%z')


class TokenSchema(BaseModel):
    email: str

    @computed_field
    @property
    def payload(self) -> dict:
        return TokenPayloadSchema(email=self.email).model_dump()

    @computed_field
    @property
    def token(self) -> str:
        return jwt.encode(self.payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
