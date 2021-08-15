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

