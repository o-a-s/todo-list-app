# Build Stage
FROM python:3.10.16-slim-bookworm AS build

WORKDIR /app/src/backend

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    VIRTUAL_ENV=/usr/local

COPY requirements.txt ./ 

# Install dependencies
RUN pip install --upgrade pip=="24.3.1" \
    && pip install uv=="0.5.14" \
    && uv pip install --python /usr/local --no-cache-dir -r requirements.txt

# Final Stage
FROM python:3.10.16-slim-bookworm

ENV PYTHONUNBUFFERED=1 \
    VIRTUAL_ENV=/usr/local

WORKDIR /app/src/backend

# Copy necessary files from the build stage
COPY --from=build /usr/local/lib/python3.10/site-packages /usr/local/lib/python3.10/site-packages
COPY --from=build /usr/local/bin /usr/local/bin

# Copy application code
COPY src/backend/ ./src/backend/

EXPOSE 3000

# CMD [ "fastapi", "dev", "backend/app/main.py", "--host", "0.0.0.0", "--port", "3000" ]
