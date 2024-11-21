from typing import Any

from app.model import Customer
from app.model.base import UuidType
from app.repository.customer_repository import CustomerRepository
from app.schema import CountResponse, CustomerCreate, CustomerResponse, CustomerUpdate
from app.utils.exceptions import NotFoundException

from .base import ServiceInterface


class CustomerService(ServiceInterface[Customer, UuidType]):
    def __init__(
        self,
        session: Any,
        repository=CustomerRepository(),
    ):
        self._session = session
        self._repository = repository

    async def create(self, obj: CustomerCreate) -> CustomerResponse:
        customer = await self._repository.create(self._session, obj)

        return CustomerResponse.model_validate(customer)

    async def read_all(
        self, limit: int = 0, offset: int = 10, filter_: dict | None = None
    ) -> list[CustomerResponse]:
        return await self._repository.get_many(
            self._session, limit=limit, offset=offset, filter_=filter_
        )

    async def read_by_id(self, obj_id: UuidType) -> CustomerResponse | None:
        customer = await self._repository.get_one_by_id(self._session, obj_id)

        if not customer:
            raise NotFoundException()

        return customer

    async def update(
        self, obj_id: UuidType, obj: CustomerUpdate
    ) -> CustomerResponse | None:
        return await self._repository.update_by_id(self._session, obj, obj_id)

    async def delete(self, obj_id: UuidType) -> bool:
        if not (await self._repository.remove_by_id(self._session, obj_id) > 0):
            raise NotFoundException()

    async def count_items(self) -> CountResponse:
        count = await self._repository.count(self._session)

        return CountResponse(count=count)
