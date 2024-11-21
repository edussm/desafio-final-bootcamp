from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.service import CustomerService
from app.utils.database import get_async_session

SessionDependency = Annotated[AsyncSession, Depends(get_async_session, use_cache=True)]


def get_customer_service(session: SessionDependency) -> CustomerService:
    return CustomerService(session)


CustomerServiceDependency = Annotated[CustomerService, Depends(get_customer_service)]
