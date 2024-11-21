from fastapi import APIRouter, Depends

from app.api.dependencies import CustomerServiceDependency
from app.schema import (
    CountResponse,
    CustomerCreate,
    CustomerFilterQueryParams,
    CustomerResponse,
    CustomerUpdate,
    PaginationQueryParams,
    UuidType,
)

router = APIRouter(prefix="/customers", tags=["Clientes"])


@router.post("", response_model=CustomerResponse, status_code=201)
async def create(customer_service: CustomerServiceDependency, customer: CustomerCreate):
    return await customer_service.create(customer)


@router.get("", response_model=list[CustomerResponse], status_code=200)
async def get(
    customer_service: CustomerServiceDependency,
    pagination: PaginationQueryParams = Depends(),
    filter_: CustomerFilterQueryParams = Depends(),
):
    return await customer_service.read_all(
        limit=pagination.limit,
        offset=pagination.offset,
        filter_=filter_.model_dump(exclude_none=True),
    )


@router.get("/{customer_id}", response_model=CustomerResponse, status_code=200)
async def get_by_id(customer_service: CustomerServiceDependency, customer_id: UuidType):
    return await customer_service.read_by_id(customer_id)


@router.get("/statistics/count", response_model=CountResponse, status_code=200)
async def get_count(customer_service: CustomerServiceDependency):
    return await customer_service.count_items()


@router.patch("/{customer_id}", response_model=CustomerResponse, status_code=200)
async def update_by_id(
    customer_service: CustomerServiceDependency,
    customer_id: UuidType,
    customer: CustomerUpdate,
):
    return await customer_service.update(customer_id, customer)


@router.delete("/{customer_id}", status_code=204)
async def delete_post(
    customer_service: CustomerServiceDependency, customer_id: UuidType
):
    await customer_service.delete(customer_id)
