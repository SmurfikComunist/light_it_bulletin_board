from abc import abstractmethod
from typing import (
    List,
    Callable,
    Optional,
)

from sqlalchemy import desc
from sqlalchemy.orm import (
    Session,
    selectinload,
)

from app.models.post import Post
from app.repository.base import (
    BaseAbstractRepository,
    BaseSqlAlchemyRepository,
)
from app.schemas.post import PostCreate


class PostAbstractRepository(BaseAbstractRepository[Post, PostCreate]):
    @abstractmethod
    def get_posts_order_by_date(self, order: Callable = desc) -> List[Post]:
        raise NotImplementedError

    @abstractmethod
    def get_with_comments(self, id: int) -> Post:
        raise NotImplementedError


class PostSqlAlchemyRepository(
    BaseSqlAlchemyRepository, PostAbstractRepository
):
    def get_posts_order_by_date(self, order: Callable = desc) -> List[Post]:
        return (
            self.session.query(self.model)
            .order_by(order(self.model.created_at))
            .all()
        )

    def get_with_comments(self, id: int) -> Post:
        return (
            self.session.query(self.model)
            .options(selectinload(Post.comments))
            .filter_by(id=id)
            .one()
        )


def get_post_sqlalchemy_repository(
    session: Session,
) -> PostSqlAlchemyRepository:
    return PostSqlAlchemyRepository(session=session, model=Post)
