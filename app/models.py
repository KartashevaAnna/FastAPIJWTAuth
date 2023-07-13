from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

Base = declarative_base()


class Post(Base):
    __tablename__ = "post"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    text = Column(String)
    user_id = Column(Integer, ForeignKey("user.id"))
    user = relationship("User")


class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True)
    password = Column(String)


class Like(Base):
    __tablename__ = "like"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    post_id = Column(Integer, ForeignKey("post.id"))

    user = relationship("User")
    post = relationship("Post")
