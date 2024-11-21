from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from app.model.base import PersistableModel, UuidType
from app.schema.base import ModelSchema
from app.schema.common import CountResponse

M = TypeVar("T", bound="PersistableModel")
ID = TypeVar("ID", bound="UuidType")


class ServiceInterface(ABC, Generic[M, ID]):
    @abstractmethod
    async def create(self, obj: ModelSchema) -> ModelSchema:
        pass

    @abstractmethod
    async def read_all(
        self, page: int = 0, per_page: int = 10, filter_: dict | None = None
    ) -> list[ModelSchema]:
        pass

    @abstractmethod
    async def read_by_id(self, obj_id: ID) -> ModelSchema | None:
        pass

    @abstractmethod
    async def update(self, obj_id: ID, obj: ModelSchema) -> ModelSchema | None:
        pass

    @abstractmethod
    async def delete(self, obj_id: ID) -> bool:
        pass

    @abstractmethod
    async def count_items(self) -> CountResponse:
        pass
