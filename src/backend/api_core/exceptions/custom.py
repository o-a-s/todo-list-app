from fastapi import status

from .base import TodoException

class NotFoundException(TodoException):
    """Base class for all Todo application errors"""
    def __init__(self, detail: str, error_code: str):
        super().__init__(
            detail=detail,
            error_code=error_code,
            status_code=status.HTTP_404_NOT_FOUND
        )

class TodoNotFoundException(NotFoundException):
    """Todo item not found"""
    def __init__(self, detail: str = "Todo not found"):
        super().__init__(
            detail=detail, 
            error_code="todo_not_found"
        )

class DatabaseException(TodoException):
    """Database operation error"""
    def __init__(self, detail: str = "Database operation failed"):
        super().__init__(
            detail=detail,
            error_code="database_error",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )