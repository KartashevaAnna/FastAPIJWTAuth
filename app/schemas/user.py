from pydantic import BaseModel, EmailStr, Field

# class UserSchema(BaseModel):
#     email: EmailStr
#
#
# class UserFullSchema(UserSchema):
#     password: str


class UserInSchema(BaseModel):
    name: str
    email: EmailStr
    password: str

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "name": "Anna",
                "email": "annakartashevamail@gmail.com",
                "password": "anypassword",
            }
        }


class UserOutSchema(BaseModel):
    name: str
    email: EmailStr


class UserLoginSchema(BaseModel):
    email: EmailStr = Field(...)
    password: str = Field(...)

    class Config:
        json_schema_extra = {
            "example": {
                "email": "annakartashevamail@gmail.com",
                "password": "anypassword",
            }
        }