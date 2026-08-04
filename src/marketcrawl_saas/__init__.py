import uvicorn


def main() -> None:
    uvicorn.run("marketcrawl_saas.app:app", host="0.0.0.0", port=8000, reload=True)
