from pydantic import BaseModel, EmailStr


class UserSchema(BaseModel):
    email: EmailStr


class UserFullSchema(UserSchema):
    password: str

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "email": "annakartashevamail@gmail.com",
                "password": "anypassword",
            }
        }
