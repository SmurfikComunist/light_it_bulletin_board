import datetime

from sqlalchemy import (
    Column,
    Integer,
    DateTime,
)
from sqlalchemy.orm import (
    as_declarative,
    declared_attr,
)


@as_declarative()
class Base:
    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(
        DateTime(timezone=True), default=datetime.datetime.utcnow
    )
    updated_at = Column(DateTime(timezone=True), nullable=True)

    __name__: str

    # Generate __tablename__ automatically
    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()
