from sqlmodel import create_engine, SQLModel
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import sessionmaker
from .config import settings
from .utils.custom_logger import CustomLogger

logger = CustomLogger(__name__)

async_engine = AsyncEngine(create_engine(url=settings.DATABASE_URL, echo=True))


async def init_db() -> None:
    try:
        logger.info("Initializing database...")
        async with async_engine.begin() as conn:
            await conn.run_sync(SQLModel.metadata.create_all)
        logger.info("Database initialized successfully.")
    except Exception as e:
        raise e("Error in initializing the database")


async_session = sessionmaker(
    bind=async_engine, class_=AsyncSession, expire_on_commit=False
)


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    try:
        logger.info("Creating database session...")
        async with async_session() as session:
            logger.info("Database session created successfully.")
            yield session
    except Exception as e:
        raise e("Error in creating the database session")
