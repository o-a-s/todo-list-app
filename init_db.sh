# Generate the initial migration
docker compose exec fastapi alembic revision --autogenerate -m "Initial migration"

# Apply the migration
docker compose exec fastapi alembic upgrade head