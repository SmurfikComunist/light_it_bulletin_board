from abc import (
    ABC,
    abstractmethod,
)
from typing import (
    TypeVar,
    Generic,
    Optional,
    Type,
)

from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.db.base_class import Base

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)


class BaseAbstractRepository(ABC, Generic[ModelType, CreateSchemaType]):
    @abstractmethod
    def get(self, id: int) -> Optional[ModelType]:
        raise NotImplementedError

    @abstractmethod
    def create(self, obj_in: CreateSchemaType) -> ModelType:
        raise NotImplementedError


class BaseSqlAlchemyRepository(BaseAbstractRepository):
    def __init__(self, session: Session, model: Type[ModelType]):
        self.session = session
        self.model = model

    def get(self, id: int) -> Optional[ModelType]:
        return (
            self.session.query(self.model).filter(self.model.id == id).first()
        )

    def create(self, obj_in: CreateSchemaType) -> ModelType:
        db_obj = self.model(**obj_in.dict())
        self.session.add(db_obj)
        self.session.commit()
        self.session.refresh(db_obj)
        return db_obj
