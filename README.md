# Todo List Application

This is a RESTful API for managing a todo list, built using FastAPI, SQLModel, and PostgreSQL.

## Table of Contents
- [Todo List Application](#todo-list-application)
  - [Table of Contents](#table-of-contents)
  - [Getting Started](#getting-started)
  - [Subsequent Migrations](#subsequent-migrations)
  - [Accessing the API](#accessing-the-api)
  - [Project Structure](#project-structure)
  - [Tech Stack](#tech-stack)
  - [Dependencies](#dependencies)
  - [API Endpoints](#api-endpoints)
    - [Todo Items](#todo-items)
  - [Database Schema](#database-schema)
  - [Logging](#logging)
  - [Contributing](#contributing)
  - [License](#license)

## Getting Started

1. **Environment Variables:**
    1. Rename the `.env.example` file to `.env`.
    2. Fill in the necessary values in the `.env` file. These variables are crucial for configuring your database connection and other settings. Here's what each variable does:
        * `POSTGRES_USER`: The username for the PostgreSQL database.
        * `POSTGRES_PASSWORD`: The password for the PostgreSQL user.
        * `POSTGRES_DB`: The name of the PostgreSQL database.
        * `DATABASE_URL`: The full connection string for the database, used by SQLModel. It should follow this format: `postgresql+asyncpg://<POSTGRES_USER>:<POSTGRES_PASSWORD>@<POSTGRES_SERVER>/<POSTGRES_DB>`

2. **Start the containers:**

    ```bash
    docker compose up -d
    ```

3. **Upgrade migrations:**

    1. **Make sure the docker containers are running.**
    2. **Apply the migration:**

        ```bash
        docker compose exec fastapi alembic upgrade head
        ```

## Subsequent Migrations

For subsequent database schema changes:

1. **Generate a new migration:**

    ```bash
    docker compose exec fastapi alembic revision --autogenerate -m "Your descriptive message"
    ```

2. **Apply the migration:**

    ```bash
    docker compose exec fastapi alembic upgrade head
    ```

    **OR you can use `init_db.sh` to run commands in steps 1 and 2**

## Accessing the API

Once the containers are up and the database is initialized, the API will be accessible at `http://localhost:3000`. You can use API client tools like `curl` to interact with the API endpoints.

You can view the interactive API documentation (Swagger) by navigating to `http://localhost:3000/docs` in your browser.

## Project Structure

The project is structured as follows:

- `src/backend/`: Contains the backend code.
    - `alembic/`: Database migration scripts and versions.
    - `app/`: Core application logic.
        - `api/`: API endpoints.
        - `deps/`: Dependency injection.
        - `exceptions/`: Custom exceptions.
        - `models/`: Database models.
        - `repositories/`: Data access layer.
        - `schemas/`: Pydantic schemas for data validation.
        - `services/`: Business logic.
        - `utils/`: Utility functions.
    - `pg_data/`: PostgreSQL data.
- `.env.example`: Modify and add your environment values.
- `requirements.txt`: Project dependencies.
- `Dockerfile`: Defines the Docker container for the FastAPI application.
- `docker-compose.yml`: Configures Docker Compose for running the FastAPI application along with PostgreSQL DB containers.
- `init_db.sh`: A script to initialize the database migrations.

## Tech Stack

- **Language**: Python 3.10.16
- **Framework**: FastAPI
- **Database**: PostgreSQL (using SQLModel)
- **ORM**: SQLModel
- **Database Driver**: asyncpg
- **Asynchronous Operations**: Asyncio

## Dependencies

The project dependencies are listed in `requirements.txt`. You can install them locally using:

```bash
pip install -r requirements.txt
```

or using `uv` for faster installation times:

```bash
pip install uv
uv pip install -r requirements.txt
```

## API Endpoints

The API endpoints are defined in `src/backend/app/api/todo.py`.

### Todo Items

- **Create Todo Item**

    - `POST /api/v1/todos`
    - Query parameters:
        - `todo_create`: Schema for the input form
    - Request body:
        ```json
        {
          "title": "string",
          "description": "string",
          "status": ["pending", "in_progress", "completed"],
          "due_date": "datetime(timezone)"
        }
        ```
    - Response:
        ```json
        {
          "title": "string",
          "description": "string",
          "priority": 0,
          "due_date": "datetime(timezone)",
          "id": "uuid",
          "status": "pending",
          "created_at": "datetime(timezone)",
          "updated_at": "datetime(timezone)"
        }
        ```

- **Read Todo Item**

    - `GET /api/v1/todos/{todo_id}`
    - Query parameters:
        - `todo_id`: UUID of the specific todo item to read
    - Response:
        ```json
        {
          "title": "string",
          "description": "string",
          "priority": 0,
          "due_date": "datetime(timezone)",
          "id": "uuid",
          "status": "pending",
          "created_at": "datetime(timezone)",
          "updated_at": "datetime(timezone)"
        }
        ```

- **Read All Todo Items**

    - `GET /api/v1/todos`
    - Query parameters:
        - `skip`: Number of items to skip (default: 0)
        - `limit`: Maximum number of items to return (default: 100)
    - Response:
        ```json
        [
          {
            "title": "string",
            "description": "string",
            "priority": 0,
            "due_date": "datetime(timezone)",
            "id": "uuid",
            "status": "pending",
            "created_at": "datetime(timezone)",
            "updated_at": "datetime(timezone)"
          }
        ]
        ```

- **Update Todo Item**

    - `PUT /api/v1/todos/{todo_id}`
    - Query parameters:
        - `todo_id`: UUID of the specific todo item to update
        - `todo_update`: Schema for the input form
    - Request body:
        ```json
        {
          "title": "string",
          "description": "string",
          "status": ["pending", "in_progress", "completed"],
          "due_date": "datetime(timezone)"
        }
        ```
    - Response:
        ```json
        {
          "title": "string",
          "description": "string",
          "priority": 0,
          "due_date": "datetime(timezone)",
          "id": "uuid",
          "status": "pending",
          "created_at": "datetime(timezone)",
          "updated_at": "datetime(timezone)"
        }
        ```

- **Delete Todo Item**

    - `DELETE /api/v1/todos/{todo_id}`
    - Query parameters:
        - `todo_id`: UUID of the specific todo item to delete
    - Response: 204 No Content

## Database Schema

The database schema is defined in `src/backend/app/models/todo.py`.

- **Todo**
    - `id`: UUID (primary key)
    - `title`: String
    - `description`: String
    - `status`: Enum (pending, in_progress, completed)
    - `priority`: int
    - `due_date`: datetime
    - `created_at`: datetime
    - `updated_at`: datetime

## Logging

The application uses a custom logger to log messages. The logging middleware logs request details and processing time.

## Contributing

Feel free to contribute to this project by submitting pull requests.

## License

This project is licensed under the Apache License 2.0.