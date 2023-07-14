from sqlalchemy import Boolean, Column, ForeignKey, Integer
from sqlalchemy.orm import relationship

from app.models import Base


class Like(Base):
    __tablename__ = "like"
    table_args = {"schema": "jwt_blog"}
    id = Column(Integer, primary_key=True, nullable=False)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    post_id = Column(Integer, ForeignKey("post.id"), nullable=False)
    is_like = Column(Boolean, nullable=True, default=None)

    user = relationship("User")
    post = relationship("Post")
