from fastapi import FastAPI, Request, status
from fastapi.responses import ORJSONResponse
import traceback

from .base import TodoException
from .custom import DatabaseException
from ..config import settings
from ..utils.custom_logger import CustomLogger

logger = CustomLogger(__name__).logger

async def create_error_response(
    request: Request, 
    exc: TodoException, 
    include_traceback: bool = False
    ) -> dict:
        error_response = {
            "detail": exc.detail,
            "error_code": exc.error_code,
            "path": request.url.path,
            "method": request.method,
        }
        
        if include_traceback:
            error_response["traceback"] = traceback.format_exc()
        
        logger.info(
            f"Error occurred: {error_response['detail']} "
            f"at endpoint: {error_response['path']} "
            f"with method: {error_response['method']}"
        )
        
        return error_response


def add_exception_handlers(app: FastAPI):
    @app.exception_handler(TodoException)
    async def todo_exception_handler(request: Request, exc: TodoException):
        error_response = await create_error_response(
            request, 
            exc,
            include_traceback=settings.ENV in ("dev", "development")
        )
        return ORJSONResponse(
            content=error_response,
            status_code=exc.status_code
        )
    
    @app.exception_handler(DatabaseException)
    async def database_exception_handler(request: Request, exc: DatabaseException):
        error_response = await create_error_response(
            request, 
            exc,
            include_traceback=settings.ENV in ("dev", "development")
        )
        return ORJSONResponse(
            content=error_response,
            status_code=exc.status_code
        )
    
    @app.exception_handler(Exception)
    async def global_exception_handler(request: Request, exc: Exception):
        is_dev = settings.ENV in ("dev", "development")
        error_response = {
            "detail": str(exc) if is_dev else "Internal Server Error",
            "error_code": "server_error",
        }
        if is_dev:
            error_response["traceback"] = traceback.format_exc()

        return ORJSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=error_response,
        )