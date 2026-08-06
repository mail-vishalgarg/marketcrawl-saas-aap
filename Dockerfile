FROM python:3.12-slim

WORKDIR /app

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Copy dependency files first for layer caching
COPY backend/pyproject.toml backend/uv.lock ./

# Install Python dependencies (no project install — app/ is not a package)
RUN uv sync --frozen --no-dev --no-install-project

# Copy application source
COPY backend/app/ ./app/

# Run as non-root
RUN useradd --no-create-home appuser && chown -R appuser:appuser /app
USER appuser

EXPOSE 8000

# app/ is on PYTHONPATH via WORKDIR=/app
ENV PYTHONPATH=/app
CMD ["/app/.venv/bin/uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
