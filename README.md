# MarketCrawl SaaS

A Python-based SaaS application for market crawling and data collection.

**Author:** Vishal Garg

![CI](https://github.com/mail-vishalgarg/marketcrawl-saas-aap/actions/workflows/ci.yml/badge.svg)

---

## Overview

MarketCrawl SaaS is a modular, extensible market data crawling platform built with Python 3.13. It provides a clean scaffolding to build scrapers, data pipelines, and SaaS-ready APIs for collecting and analyzing market intelligence.

---

## Requirements

- Python 3.13+
- [uv](https://docs.astral.sh/uv/) — fast Python package and project manager
- [Docker](https://www.docker.com/) — optional, for containerized runs

---

## Quick Start

### 1. Clone the repository

```bash
git clone https://github.com/mail-vishalgarg/marketcrawl-saas-aap.git
cd marketcrawl-saas-aap
```

### 2. Install `uv` (if not already installed)

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
source $HOME/.local/bin/env
```

### 3. Create and activate the virtual environment

```bash
uv venv
source .venv/bin/activate       # macOS/Linux
# .venv\Scripts\activate        # Windows
```

### 4. Install dependencies

```bash
uv sync
```

### 5. Configure environment variables

```bash
cp .env.example .env   # copy the example file
# Edit .env and fill in your API keys / secrets
```

### 6. Run the application

```bash
uv run python -m marketcrawl_saas
```

The server starts on `http://localhost:8000` with hot-reload enabled.

### 7. Verify it's running

```bash
curl http://localhost:8000/health
```

Expected response:

```json
{
  "status": "ok",
  "version": "0.1.0",
  "service": "MarketCrawl SaaS"
}
```

Auto-generated API docs:

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

---

## Running with Docker

Build and run the container locally:

```bash
docker build -t marketcrawl-saas .
docker run -p 8000:8000 marketcrawl-saas
```

Then hit the health endpoint:

```bash
curl http://localhost:8000/health
```

The container runs as a non-root user and exposes port `8000`.

---

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/health` | Returns service status and version |

---

## Project Structure

```
marketcrawl-saas/
├── .github/
│   └── workflows/
│       └── ci.yml            # GitHub Actions CI pipeline
├── src/
│   └── marketcrawl_saas/
│       ├── __init__.py       # Entry point — boots uvicorn
│       └── app.py            # FastAPI app and routes
├── .env                      # Local environment variables (gitignored)
├── .env.example              # Example environment variables template
├── .gitignore
├── .python-version           # Pinned Python version (3.13)
├── Dockerfile                # Container definition
├── pyproject.toml            # Project metadata and dependencies
├── uv.lock                   # Locked dependency versions
└── README.md
```

---

## CI / CD

Every push and pull request to `main` triggers the GitHub Actions CI pipeline with two jobs:

| Job | Checks |
|-----|--------|
| **Lint & Type Check** | `ruff format`, `ruff check`, `pyright` |
| **Docker Build** | Builds the image and smoke-tests `/health` |

View runs: [GitHub Actions](https://github.com/mail-vishalgarg/marketcrawl-saas-aap/actions)

---

## Development

### Add a dependency

```bash
uv add <package-name>
```

### Remove a dependency

```bash
uv remove <package-name>
```

### Run linting and type checks locally

```bash
uv run ruff format .
uv run ruff check .
uv run pyright src/
```

### Run tests (once added)

```bash
uv run pytest
```

---

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/my-feature`
3. Commit your changes: `git commit -m "feat: add my feature"`
4. Push to the branch: `git push origin feature/my-feature`
5. Open a Pull Request

---

## License

MIT

---

*Built by [Vishal Garg](https://github.com/mail-vishalgarg)*
