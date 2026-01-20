# Backend Dockerfile for FastAPI
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Install system dependencies for python-magic and health checks
RUN apt-get update && apt-get install -y \
    libmagic1 \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install uv for fast package management
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Copy dependency files first (for better caching)
COPY pyproject.toml uv.lock* ./

# Install dependencies (not using --frozen to allow platform-specific resolution)
RUN uv sync --no-dev

# Copy application code into capi subdirectory to maintain package structure
COPY . ./capi/

# Create non-root user for security
RUN useradd --create-home --shell /bin/bash appuser
RUN chown -R appuser:appuser /app
USER appuser

# Expose port
EXPOSE 8000

# Run the application
CMD ["uv", "run", "uvicorn", "capi.main:app", "--host", "0.0.0.0", "--port", "8000"]
