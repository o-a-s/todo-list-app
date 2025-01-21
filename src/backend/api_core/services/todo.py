from uuid import UUID

from ..models.todo import Todo
from ..repos.todo import TodoRepository
from ..schemas.todo import TodoCreate, TodoUpdate
from ..utils.custom_logger import CustomLogger
from ..exceptions.custom import TodoNotFoundException

class TodoService:
    def __init__(self, todo_repository: TodoRepository):
        self.logger = CustomLogger(__name__).logger
        self.todo_repository = todo_repository

    async def create_todo(self, todo_create: TodoCreate) -> Todo:
        """Creates a new todo item.

        Args:
            todo_create: Data for creating a new todo.

        Returns:
            The created todo item.
        """
        created_todo = await self.todo_repository.create_todo(todo_create)
        self.logger.info(f"Todo item created with id: {created_todo.id}")
        return created_todo


    async def read_todos(self, skip: int = 0, limit: int = 100) -> list[Todo]:
        """Retrieves a list of todo items.

        Args:
            skip: The number of items to skip.
            limit: The maximum number of items to return.

        Returns:
            A list of todo items.
        """
        todos = await self.todo_repository.read_todos(skip, limit)
        self.logger.info(f"Found {len(todos)} todo items")
        return todos


    async def read_todo(self, todo_id: UUID) -> Todo:
        """Retrieves a specific todo item by ID.

        Args:
            todo_id: The ID of the todo item to retrieve.

        Returns:
            The requested todo item.

        Raises:
            HTTPException: If the todo item is not found.
        """
        todo = await self.todo_repository.read_todo(todo_id)
        if not todo:
            raise TodoNotFoundException()
        self.logger.info(f"Todo item found with id: {todo_id}")
        return todo


    async def update_todo(self, todo_id: UUID, todo_update: TodoUpdate) -> Todo:
        """Updates a specific todo item.

        Args:
            todo_id: The ID of the todo item to update.
            todo_update: The data to update the todo item with.

        Returns:
            The updated todo item.
        """
        updated_todo = await self.todo_repository.update_todo(todo_id, todo_update)
        if not updated_todo:
            raise TodoNotFoundException()
        self.logger.info(f"Todo item updated with id: {updated_todo.id}")
        return updated_todo


    async def delete_todo(self, todo_id: UUID) -> None:
        """Deletes a specific todo item.

        Args:
            todo_id: The ID of the todo item to delete.

        Raises:
            HTTPException: If the todo item is not found.
        """
        delete_success = await self.todo_repository.delete_todo(todo_id)
        if not delete_success:
            raise TodoNotFoundException()
        self.logger.info(f"Todo item deleted with id: {todo_id}")
