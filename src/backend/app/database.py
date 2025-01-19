from sqlmodel import create_engine, SQLModel
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy.exc import SQLAlchemyError
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import sessionmaker

from .config import settings
from .utils.custom_logger import CustomLogger
from .exceptions.custom import DatabaseException

logger = CustomLogger(__name__).logger

async_engine = AsyncEngine(create_engine(url=settings.DATABASE_URL, echo=True))


async def init_db() -> None:
    try:
        async with async_engine.begin() as conn:
            await conn.run_sync(SQLModel.metadata.create_all)
        logger.info("Database initialized successfully.")
    except SQLAlchemyError as e:
        raise DatabaseException(detail=str(e))


async_session = sessionmaker(
    bind=async_engine, class_=AsyncSession, expire_on_commit=False
)


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    try:
        async with async_session() as session:
            logger.info("Database session created successfully.")
            yield session
    except SQLAlchemyError as e:
        raise DatabaseException(detail=str(e))
