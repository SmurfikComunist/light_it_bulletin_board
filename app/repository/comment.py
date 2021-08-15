from typing import Optional

from sqlalchemy.orm import Session

from app.models.comment import Comment
from app.repository.base import (
    BaseAbstractRepository,
    BaseSqlAlchemyRepository,
)
from app.schemas.comment import CommentCreate


class CommentAbstractRepository(
    BaseAbstractRepository[Comment, CommentCreate]
):
    pass


