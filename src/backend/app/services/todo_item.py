import logging
from uuid import UUID

from ..models.todo_item import TodoItem
from ..repositories.todo_item import TodoRepository
from ..schemas.todo_item import TodoCreate
from ..utils.custom_logger import CustomLogger

class TodoService:
    def __init__(self, todo_repository: TodoRepository):
        self.logger = CustomLogger(__name__)
        self.todo_repository = todo_repository

    async def create_todo(self, todo_create: TodoCreate) -> TodoItem:
        """Creates a new todo item.

        Args:
            todo_create: Data for creating a new todo.

        Returns:
            The created todo item.
        """
        return await self.todo_repository.create_todo(todo_create)

    async def read_todo(self, todo_id: UUID) -> TodoItem:
        """Retrieves a specific todo item by ID.

        Args:
            todo_id: The ID of the todo item to retrieve.

        Returns:
            The requested todo item.

        Raises:
            HTTPException: If the todo item is not found.
        """
        return await self.todo_repository.read_todo(todo_id)

    async def read_todos(self, skip: int = 0, limit: int = 100) -> list[TodoItem]:
        """Retrieves a list of todo items.

        Args:
            skip: The number of items to skip.
            limit: The maximum number of items to return.

        Returns:
            A list of todo items.
        """
        return await self.todo_repository.read_todos(skip, limit)

    async def update_todo(self, todo_id: UUID, update_data: dict) -> TodoItem:
        """Updates a specific todo item.

        Args:
            todo_id: The ID of the todo item to update.
            todo_update: The data to update the todo item with.

        Returns:
            The updated todo item.
        """
        return await self.todo_repository.update_todo(todo_id, update_data)

    async def delete_todo(self, todo_id: UUID) -> None:
        """Deletes a specific todo item.

        Args:
            todo_id: The ID of the todo item to delete.

        Raises:
            HTTPException: If the todo item is not found.
        """
        return await self.todo_repository.delete_todo(todo_id)
