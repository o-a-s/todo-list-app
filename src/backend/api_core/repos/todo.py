from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from sqlmodel import select, update

from ..models.todo import Todo
from ..schemas.todo import TodoCreate, TodoUpdate
from ..exceptions.custom import DatabaseException


class TodoRepository:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def create_todo(self, todo_create: TodoCreate) -> Todo:
        """
        Creates a new todo item in the database.

        Args:
            todo_create (TodoCreate): The schema containing the data for the new todo item.

        Returns:
            Todo: The newly created todo item.

        Raises:
            SQLAlchemyError: If there is an error during database operations.
        """
        try:
            todo = Todo(**todo_create.model_dump())
            self.db_session.add(todo)
            await self.db_session.commit()
            
            return todo
        except SQLAlchemyError as e:
            await self.db_session.rollback()
            raise DatabaseException(detail=str(e))


    async def read_todos(self, skip: int = 0, limit: int = 100) -> list[Todo] | list[None]:
        """
        Reads all todo items in the database.

        Args:
            skip (int): The value for how many todo items to skip before reading.
            limit (int): The value for how many todo item to display.

        Returns:
            Todo: A list of all avaiable todo items or an empty list.

        Raises:
            SQLAlchemyError: If there is an error during database operations.
        """
        try:
            query = select(Todo).offset(skip).limit(limit)
            result = await self.db_session.execute(query)
            todos = result.scalars().all()
            
            return todos
        except SQLAlchemyError as e:
            raise DatabaseException(detail=str(e))


    async def read_todo(self, todo_id: UUID) -> Todo | None:
        """
        Reads a new todo item in the database.

        Args:
            todo_id (UUID): The uuid for the todo item.

        Returns:
            Todo: The specified todo item.

        Raises:
            SQLAlchemyError: If there is an error during database operations.
        """
        try:
            todo = await self.db_session.get(Todo, todo_id)
            
            return todo
        except SQLAlchemyError as e:
            raise DatabaseException(detail=str(e))


    async def update_todo(self, todo_id: UUID, todo_update: TodoUpdate) -> Todo | None:
        """
        Updates a todo item's one or more fields as specified.

        Args:
            todo_id (UUID): The uuid for the todo item.
            update_data (dict): The schema containing the fields that can be updated.

        Returns:
            Todo: The specified todo item.

        Raises:
            SQLAlchemyError: If there is an error during database operations.
        """
        try:
            update_data = todo_update.model_dump(exclude_unset=True)
            query = (
                update(Todo)
                .where(Todo.id == todo_id)
                .values(**update_data)
                .returning(Todo)
            )

            result = await self.db_session.execute(query)
            updated_todo = result.scalar_one_or_none()
            await self.db_session.commit()

            return updated_todo
        except SQLAlchemyError as e:
            await self.db_session.rollback()
            raise DatabaseException(detail=str(e))


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
            todo = await self.db_session.get(Todo, todo_id)
            if not todo:
                return False
            await self.db_session.delete(todo)
            await self.db_session.commit()
            
            return True
        except SQLAlchemyError as e:
            await self.db_session.rollback()
            raise DatabaseException(detail=str(e))
