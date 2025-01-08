from uuid import UUID, uuid4
from datetime import datetime
from enum import Enum
from sqlmodel import SQLModel, Field, Column
from sqlalchemy.dialects import postgresql as pg
from sqlalchemy import func

class TodoStatus(str, Enum):
    """
    Represents the status of a todo item.
    """
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"


class TodoItem(SQLModel, table=True):
    """
    Represents a todo item in the database.
    """
    __tablename__ = "todoitems"

    id: UUID = Field(
        sa_column=Column(pg.UUID, primary_key=True, default=uuid4, index=True),
    )
    title: str = Field(
        sa_column=Column(pg.VARCHAR(255), nullable=False, index=True),
        max_length=255,
        min_length=1,
    )
    description: str | None = Field(
        sa_column=Column(pg.TEXT, default=None),
        max_length=5000,
    )
    status: TodoStatus = Field(
        sa_column=Column(pg.VARCHAR(20), server_default=TodoStatus.PENDING.value, nullable=False, index=True),
        description="Current status of the todo item (pending, in_progress, completed)"
    )
    priority: int = Field(
        sa_column=Column(pg.INTEGER, server_default="0", nullable=False, index=True),
        ge=0,
        le=5,
        description="Priority of the todo item (0: None, 1-5: higher values indicate higher priority)"
    )
    due_date: datetime | None = Field(
        sa_column=Column(pg.TIMESTAMP(timezone=True), default=None, index=True),
    )
    created_at: datetime = Field(
        sa_column=Column(pg.TIMESTAMP(timezone=True), server_default=func.now()),
    )
    updated_at: datetime = Field(
        sa_column=Column(pg.TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now()),
    )