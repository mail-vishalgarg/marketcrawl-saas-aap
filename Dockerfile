FROM python:3.13-slim

WORKDIR /app

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Copy dependency files first for layer caching
COPY pyproject.toml uv.lock ./

# Install dependencies only (skip building the project itself for better layer caching)
RUN uv sync --frozen --no-dev --no-install-project

# Copy application source
COPY src/ ./src/

# Install the project itself
RUN uv sync --frozen --no-dev

# Run as non-root — chown so appuser can access the venv
RUN useradd --no-create-home appuser && chown -R appuser:appuser /app
USER appuser

EXPOSE 8000

# Use venv's uvicorn directly — no uv run needed at runtime
CMD ["/app/.venv/bin/uvicorn", "marketcrawl_saas.app:app", "--host", "0.0.0.0", "--port", "8000"]
