from uuid import UUID

from fastapi import APIRouter, Depends, status

from ..deps.todo import get_todo_service
from ..services.todo import TodoService
from ..schemas.todo import TodoCreate, TodoRead, TodoUpdate

router = APIRouter()


@router.post("/", response_model=TodoRead, status_code=status.HTTP_201_CREATED)
async def create_todo(
    todo_create: TodoCreate, todo_service: TodoService = Depends(get_todo_service)
):
    """Creates a new todo item."""
    return await todo_service.create_todo(todo_create)


@router.get("/", response_model=list[TodoRead])
async def read_todos(
    skip: int = 0,
    limit: int = 100,
    todo_service: TodoService = Depends(get_todo_service),
):
    """Retreives all todo items."""
    return await todo_service.read_todos(skip, limit)


@router.get("/{todo_id}", response_model=TodoRead)
async def read_todo(
    todo_id: UUID, todo_service: TodoService = Depends(get_todo_service)
):
    """Retrieves a specific todo item by ID."""
    return await todo_service.read_todo(todo_id)


@router.put("/{todo_id}", response_model=TodoRead)
async def update_todo(
    todo_id: UUID,
    todo_update: TodoUpdate,
    todo_service: TodoService = Depends(get_todo_service),
):
    """Updates a specific todo item."""
    return await todo_service.update_todo(todo_id, todo_update)


@router.delete("/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(
    todo_id: UUID, todo_service: TodoService = Depends(get_todo_service)
):
    """Deletes a specific todo item."""
    await todo_service.delete_todo(todo_id)
