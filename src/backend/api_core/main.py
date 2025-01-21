from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from .database import init_db
from .middleware import register_middleware
from .api.todo import router as todo_router
from .utils.custom_logger import CustomLogger
from .exceptions.handler import add_exception_handlers

from contextlib import asynccontextmanager

logger = CustomLogger(__name__).logger

@asynccontextmanager
async def life_span(app: FastAPI):
    logger.info("Server is starting...")
    try:
        await init_db()
        yield
    except Exception as e:
        logger.error(f"Error during server startup: {e}")
        raise
    finally:
        logger.info("Server has been stopped.")

def create_app() -> FastAPI:
    version = "v1"

    description = "A backend api for a todo list app"

    version_prefix =f"/api/{version}"

    app = FastAPI(
        title="Todo list",
        description=description,
        version=version,
        lifespan=life_span,
        default_response_class=ORJSONResponse
    )

    register_middleware(app)
    
    add_exception_handlers(app)

    app.include_router(
        todo_router, prefix=f"{version_prefix}/todos", tags=["todos"]
    )
    
    return app

app = create_app()
