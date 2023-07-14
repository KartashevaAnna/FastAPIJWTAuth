from sqlalchemy import Column, Integer, String

from app.models import Base


class User(Base):
    __tablename__ = "user"
    table_args = {"schema": "jwt_blog"}
    id = Column(Integer, primary_key=True, unique=True)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
