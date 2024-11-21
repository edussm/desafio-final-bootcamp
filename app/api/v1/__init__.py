from fastapi import APIRouter

from app.api.v1.customer import router as customers_router

router = APIRouter(prefix="/v1")

router.include_router(customers_router)
