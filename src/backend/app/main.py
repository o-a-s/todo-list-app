from fastapi import FastAPI
from .database import init_db
from .middleware import register_middleware
from .api.todo_item import router as todo_router
from .utils.custom_logger import CustomLogger

from contextlib import asynccontextmanager

logger = CustomLogger(__name__)

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


version = "v1"

description = "A backend api for a todo list app"

version_prefix =f"/api/{version}"

app = FastAPI(
    title="Todo list",
    description=description,
    version=version,
    lifespan=life_span,
)

register_middleware(app)

app.include_router(
    todo_router, prefix=f"{version_prefix}/todo_items", tags=["todo_items"]
)
