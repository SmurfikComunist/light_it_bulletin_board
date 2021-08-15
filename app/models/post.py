from typing import TYPE_CHECKING

from sqlalchemy import (
    Column,
    Text,
    String,
)
from sqlalchemy.orm import relationship

from app.db.base_class import Base

if TYPE_CHECKING:
    from .comment import Comment  # noqa


class Post(Base):
    author = Column(String(length=100))
    title = Column(String(length=100))
    text = Column(Text(length=1000))
    comments = relationship("Comment", back_populates="post")
