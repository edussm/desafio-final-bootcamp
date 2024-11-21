import logging
from contextlib import asynccontextmanager

from asgi_correlation_id import CorrelationIdMiddleware
from fastapi import FastAPI, HTTPException

from app.api import router as api_router
from app.utils import (
    config,
    logger_exception_handler,
    register_custom_exception_handlers,
    setup_logger,
)

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(_: FastAPI):
    setup_logger()
    logger.warning(f"Starting the application: ENV={config.ENV}")
    yield
    logger.warning("Shutting down the application")


app = FastAPI(lifespan=lifespan)

app.add_middleware(CorrelationIdMiddleware, header_name="X-Correlation-ID")
app.exception_handler(HTTPException)(logger_exception_handler)
register_custom_exception_handlers(app)
app.include_router(api_router)
