FROM python:3.13-slim

WORKDIR /app

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Copy dependency files first for layer caching
COPY pyproject.toml uv.lock ./

# Install dependencies (no dev extras, no editable install)
RUN uv sync --frozen --no-dev --no-editable

# Copy application source
COPY src/ ./src/

# Run as non-root
RUN useradd --no-create-home appuser
USER appuser

EXPOSE 8000

CMD ["uv", "run", "uvicorn", "marketcrawl_saas.app:app", "--host", "0.0.0.0", "--port", "8000"]
