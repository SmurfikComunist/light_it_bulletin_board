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


class CommentSqlAlchemyRepository(
    BaseSqlAlchemyRepository, CommentAbstractRepository
):
    pass


def get_comment_sqlalchemy_repository(
    session: Session,
) -> CommentSqlAlchemyRepository:
    return CommentSqlAlchemyRepository(session=session, model=Comment)
