from typing import TYPE_CHECKING

from sqlalchemy import (
    Integer,
    Column,
    Text,
    String,
    ForeignKey,
)
from sqlalchemy.orm import relationship

from app.db.base_class import Base

if TYPE_CHECKING:
    from .post import Post  # noqa


class Comment(Base):
    author = Column(String(length=100))
    text = Column(Text(length=200))
    post_id = Column(Integer, ForeignKey("post.id"))
    post = relationship("Post", back_populates="comments")
