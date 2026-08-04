# MarketCrawl SaaS

A Python-based SaaS application for market crawling and data collection.

**Author:** Vishal Garg

---

## Overview

MarketCrawl SaaS is a modular, extensible market data crawling platform built with Python 3.13. It provides a clean scaffolding to build scrapers, data pipelines, and SaaS-ready APIs for collecting and analyzing market intelligence.

---

## Requirements

- Python 3.13+
- [uv](https://docs.astral.sh/uv/) — fast Python package and project manager

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

Or with the virtual environment activated:

```bash
python -m marketcrawl_saas
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

You can also browse the auto-generated API docs at:

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

---

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/health` | Returns service status and version |

---

## Project Structure

```
marketcrawl-saas/
├── src/
│   └── marketcrawl_saas/
│       ├── __init__.py       # Entry point — boots uvicorn
│       └── app.py            # FastAPI app and routes
├── .env                      # Local environment variables (gitignored)
├── .env.example              # Example environment variables template
├── .gitignore
├── .python-version           # Pinned Python version (3.13)
├── pyproject.toml            # Project metadata and dependencies
└── README.md
```

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

### Run the CLI entry point

```bash
marketcrawl-saas
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
