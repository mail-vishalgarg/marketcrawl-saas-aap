# Security Rules

- **Never commit secrets.** API keys, tokens, and passwords belong only in `.env`
  (gitignored). Fail any PR that adds a secret to tracked files.
- **Read config from environment only.** Use `os.getenv()` or a Pydantic `Settings` class
  backed by env vars. Never hardcode values or read from files outside the repo boundary.
- **Hash API keys before storage.** Store a SHA-256 hash of customer API keys in the
  database; compare hashes at auth time. Never store the raw key.
- **Validate all external input.** Every payload from Oxylabs, OpenAI, or user HTTP requests
  must pass through a Pydantic model before use. Reject unknown fields (`model_config =
  ConfigDict(extra="forbid")`).
