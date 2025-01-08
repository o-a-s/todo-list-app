import logging
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from ..database import get_db_session
from ..repositories.todo_item import TodoRepository
from ..services.todo_item import TodoService
from ..schemas.todo_item import TodoCreate, TodoRead, TodoUpdate
from ..utils.custom_logger import CustomLogger

logger = CustomLogger(__name__)

router = APIRouter()


def get_todo_repository(
    db_session: AsyncSession = Depends(get_db_session),
) -> TodoRepository:
    return TodoRepository(db_session)


def get_todo_service(
    todo_repository: TodoRepository = Depends(get_todo_repository),
) -> TodoService:
    return TodoService(todo_repository)


@router.post("/", response_model=TodoRead, status_code=status.HTTP_201_CREATED)
async def create_todo(
    todo_create: TodoCreate, todo_service: TodoService = Depends(get_todo_service)
):
    """Creates a new todo item."""
    logger.info(f"Creating todo item with data: {todo_create}")
    
    created_todo = await todo_service.create_todo(todo_create)
    if not created_todo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo item not found")
    return created_todo


@router.get("/{todo_id}", response_model=TodoRead)
async def read_todo(
    todo_id: UUID, todo_service: TodoService = Depends(get_todo_service)
):
    """Retrieves a specific todo item by ID."""
    logger.info(f"Reading todo item with id: {todo_id}")
    
    todo = await todo_service.read_todo(todo_id)
    if not todo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo item not found")
    return todo


@router.get("/", response_model=list[TodoRead])
async def read_todos(
    skip: int = 0,
    limit: int = 100,
    todo_service: TodoService = Depends(get_todo_service),
):
    """Retreives all todo items."""
    logger.info(f"Reading todo items with skip: {skip}, limit: {limit}")
    
    todos = await todo_service.read_todos(skip, limit)
    if not todos:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo item not found")
    return todos


@router.put("/{todo_id}", response_model=TodoRead)
async def update_todo(
    todo_id: UUID,
    todo_update: TodoUpdate,
    todo_service: TodoService = Depends(get_todo_service),
):
    """Updates a specific todo item."""
    logger.info(f"Updating todo item with id: {todo_id}, data: {todo_update}")
    
    update_data = todo_update.model_dump(exclude_unset=True)
    if not update_data:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No fields provided for update")
    
    updated_todo = await todo_service.update_todo(todo_id, update_data)
    if not updated_todo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo item not found")
    
    return updated_todo


@router.delete("/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(
    todo_id: UUID, todo_service: TodoService = Depends(get_todo_service)
):
    """Deletes a specific todo item."""
    logger.info(f"Deleting todo item with id: {todo_id}")
    
    item_deleted = await todo_service.delete_todo(todo_id)
    if not item_deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo item not found")
