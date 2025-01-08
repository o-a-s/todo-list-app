from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict
from ..models.todo_item import TodoStatus


class TodoBase(BaseModel):
    """Base Todo schema with common fields"""
    model_config = ConfigDict(from_attributes=True)
    
    title: str = Field(
        max_length=255, 
        min_length=1
        )
    description: str | None = Field(
        default=None,
        max_length=5000,
    )
    priority: int = Field(
        default=0,
        ge=0,
        le=5,
        description="Priority of the todo item (0: None, 1-5: higher values indicate higher priority)"
    )
    due_date: datetime | None = None

class TodoCreate(TodoBase):
    """Schema for creating a todo item"""
    # Fields will maintain the same order as TodoBase
    pass


class TodoRead(TodoBase):
    """
    Schema for reading a todo item, including all fields from the database.
    """
    id: UUID
    status: TodoStatus
    due_date: datetime | None = None
    created_at: datetime
    updated_at: datetime


class TodoUpdate(BaseModel):
    """Schema for updating a todo item"""
    model_config = ConfigDict(from_attributes=True)
    
    title: str | None = Field(
        default=None, 
        max_length=255, 
        min_length=1
    )
    description: str | None = None
    status: TodoStatus | None = Field(
        default=None,
        description="Current status of the todo item (pending, in_progress, completed)"
    )
    priority: int | None = Field(
        default=None,
        description="Priority of the todo item (0: None, 1-5: higher values indicate higher priority",
    )
    due_date: datetime | None = None
