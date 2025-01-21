from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends

from ..database import get_db_session
from ..repos.todo import TodoRepository
from ..services.todo import TodoService


def get_todo_repository(
    db_session: AsyncSession = Depends(get_db_session),
) -> TodoRepository:
    return TodoRepository(db_session)


def get_todo_service(
    todo_repository: TodoRepository = Depends(get_todo_repository),
) -> TodoService:
    return TodoService(todo_repository)