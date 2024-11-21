import logging

from fastapi import FastAPI, HTTPException, Request, Response
from fastapi.exception_handlers import http_exception_handler
from fastapi.responses import JSONResponse

from .exceptions import IntegrityConflictException, ModelException, NotFoundException

logger = logging.getLogger(__name__)


async def logger_exception_handler(request: Request, exc: HTTPException) -> Response:
    logger.error(f"HTTPException: {exc.status_code} - {exc.detail}")
    return await http_exception_handler(request, exc)


# TODO: detalhar melhor os erros
def register_custom_exception_handlers(app: FastAPI):
    @app.exception_handler(NotFoundException)
    async def not_found_exception_handler(request, exc: NotFoundException):
        return JSONResponse(status_code=404, content={"message": "Item not found!"})

    @app.exception_handler(IntegrityConflictException)
    async def integrity_conflict_exception_handler(
        request, exc: IntegrityConflictException
    ):
        return JSONResponse(
            status_code=400, content={"message": "Item already exists!"}
        )

    @app.exception_handler(ModelException)
    async def generic_model_exception_handler(request, exc: ModelException):
        return JSONResponse(status_code=500, content={"message": "Internal error!"})
