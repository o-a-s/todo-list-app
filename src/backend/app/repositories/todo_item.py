import logging
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from sqlmodel import select, update

from ..models.todo_item import TodoItem
from ..schemas.todo_item import TodoCreate
from ..utils.custom_logger import CustomLogger


class TodoRepository:
    def __init__(self, db_session: AsyncSession):
        self.logger = CustomLogger(__name__)
        self.db_session = db_session

    async def create_todo(self, todo_create: TodoCreate) -> TodoItem:
        """
        Creates a new todo item in the database.

        Args:
            todo_create (TodoCreate): The schema containing the data for the new todo item.

        Returns:
            TodoItem: The newly created todo item.

        Raises:
            SQLAlchemyError: If there is an error during database operations.
        """
        try:
            todo = TodoItem(**todo_create.model_dump())
            self.db_session.add(todo)
            await self.db_session.commit()
            
            self.logger.info(f"Todo item created with id: {todo.id}")
            return todo
        except SQLAlchemyError as e:
            await self.db_session.rollback()
            raise e

    async def read_todo(self, todo_id: UUID) -> TodoItem | None:
        """
        Reads a new todo item in the database.

        Args:
            todo_id (UUID): The uuid for the todo item.

        Returns:
            TodoItem: The specified todo item.

        Raises:
            SQLAlchemyError: If there is an error during database operations.
        """
        try:
            todo = await self.db_session.get(TodoItem, todo_id)
            
            self.logger.info(f"Todo item found with id: {todo_id}")
            return todo
        except SQLAlchemyError as e:
            raise e

    async def read_todos(self, skip: int = 0, limit: int = 100) -> list[TodoItem]:
        """
        Reads all todo items in the database.

        Args:
            skip (int): The value for how many todo items to skip before reading.
            limit (int): The value for how many todo item to display.

        Returns:
            TodoItem: All todo items.

        Raises:
            SQLAlchemyError: If there is an error during database operations.
        """
        try:
            query = select(TodoItem).offset(skip).limit(limit)
            result = await self.db_session.execute(query)
            todos = result.scalars().all()
            
            self.logger.info(f"Found {len(todos)} todo items")
            return todos
        except SQLAlchemyError as e:
            raise e

    async def update_todo(self, todo_id: UUID, update_data: dict) -> TodoItem | None:
        """
        Updates a todo item's one or more fields as specified.

        Args:
            todo_id (UUID): The uuid for the todo item.
            update_data (dict): The schema containing the fields that can be updated.

        Returns:
            TodoItem: The specified todo item.

        Raises:
            SQLAlchemyError: If there is an error during database operations.
        """
        try:
            query = (
                update(TodoItem)
                .where(TodoItem.id == todo_id)
                .values(**update_data)
                .returning(TodoItem)
            )

            result = await self.db_session.execute(query)
            updated_todo = result.scalar_one_or_none()

            await self.db_session.commit()

            self.logger.info(f"Todo item updated with id: {updated_todo.id}")
            return updated_todo
        except SQLAlchemyError as e:
            await self.db_session.rollback()
            raise e

    async def delete_todo(self, todo_id: UUID) -> bool:
        """
        Deletes a specified todo item in the database.

        Args:
            todo_id (UUID): The uuid for the todo item.

        Returns:
            True, if the deletion was successful.

        Raises:
            SQLAlchemyError: If there is an error during database operations.
        """
        try:
            todo = await self.db_session.get(TodoItem, todo_id)

            await self.db_session.delete(todo)
            await self.db_session.commit()
            self.logger.info(f"Todo item deleted with id: {todo_id}")
            return True
        except SQLAlchemyError as e:
            await self.db_session.rollback()
            raise e
