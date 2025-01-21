# ------------- Build Stage -------------
FROM python:3.10-slim AS builder

# Create virutal environment
RUN python -m venv /opt/venv
ENV PATH=/opt/venv/bin:$PATH

# Install dependencies
COPY requirements.txt .
RUN pip install --upgrade pip==24.3.1 uv==0.5.14 && \
    uv pip install --no-cache-dir -r requirements.txt

# Clean up
RUN find /opt/venv -type d -name "__pycache__" -exec rm -rf {} + && \
    rm -rf /opt/venv/bin/pip* /opt/venv/bin/wheel* /opt/venv/bin/uv


# ------------- Runtime Stage -------------
FROM python:3.10-slim

# Create non-root user
RUN groupadd -r appuser && useradd -r -g appuser appuser

# Enivronment setup
ENV PATH="/opt/venv/bin:$PATH" \
    PYTHONUNBUFFERED="1" \
    PYTHONDONTWRITEBYTECODE="1"

# Copy necessary files from the build stage
COPY --from=builder --chown=appuser:appuser /opt/venv /opt/venv

# Copy application code
COPY --chown=appuser:appuser src/backend/ /app/

WORKDIR /app
USER appuser

EXPOSE 3000

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl --fail http://localhost:3000/health || exit 1

# CMD [ "fastapi", "dev", "backend/app/main.py", "--host", "0.0.0.0", "--port", "3000" ]
