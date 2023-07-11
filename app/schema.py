from pydantic import BaseModel, EmailStr, Field


class PostSchema(BaseModel):
    title: str = Field(...)
    content: str = Field(...)
    author_id: int

    class Config:
        from_attributes = True


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
