# Level 9 — The AI Agent & Its Tools

**Goal:** replace the Level 8 stub with the real thing — a LangGraph agent that scrapes Amazon
via Oxylabs, remembers conversations, and powers both the playground chat and `/v1/extract`.
This is where the extracted `marketcrawl` prompts (see `reference/marketcrawl_prompts.md`) go.

## Prompt to paste into Claude Code

```text
Build the AI agent that powers MarketPulse and wire it into the existing API.

Backend (backend/app/agent/):
- oxylabs_client.py: one scrape(source, query/asin, ...) function over the Oxylabs Web
  Scraper API using OXYLABS_USERNAME/PASSWORD. If credentials are missing, run in MOCK mode
  from saved fixtures under agent/fixtures/ so the whole app works with zero credits.
- tools.py: four LangChain @tool functions. IMPORTANT: copy the tool docstrings verbatim from
  prompts/reference/marketpulse_prompts.md — the docstring IS the prompt that tells the LLM
  when to use each tool. The tools:
    1. search_products(query, max_results=8)
    2. get_product_details(asin)          # accept a raw ASIN or a full Amazon URL
    3. find_competitors(asin, max_competitors=5)
    4. download_product_images(asin, max_images=4)
  Each returns a COMPACT JSON string (slim to ~12 fields), never the raw scrape. Wrap each in
  a decorator that catches exceptions and returns {"error": ...} instead of raising.
- graph.py: a LangGraph ReAct agent (START -> summarize -> agent <-> tools -> END).
  Use the system prompt from reference/marketpulse_prompts.md (templated on the marketplace).
  Add a summarization node that, once the thread exceeds MAX_MESSAGES (12), folds old messages
  into a running summary and deletes them with RemoveMessage, keeping the last KEEP_LAST (6).
- memory.py: a checkpointer factory using langgraph-checkpoint-postgres against POSTGRES_URI
  (our Supabase DB), so conversations survive restarts, keyed by thread_id.

Wire it in:
- services/extract.py: replace the stub run() body with a single agent turn that returns
  structured product JSON. Keep the signature so /v1/extract is unchanged.
- Add POST /chat (JWT-protected) for the dashboard playground: {thread_id, message} ->
  streamed/loop agent response, tool trace, product cards, image paths.
- Serve downloaded images at /downloads.

Tests (run in MOCK mode): search returns products; a multi-tool turn works; memory persists a
fact across a simulated restart; summarization fires past 12 messages.
```

## Acceptance criteria
- `POST /v1/extract` returns real (or mock) structured product data via the agent.
- Playground chat runs the tool loop; conversations persist in Postgres across restarts.
- Runs fully in mock mode with no Oxylabs account.

## Teaching notes
- The **tool docstring is the prompt** — this is the single best agent-engineering lesson.
  Show how rewording a docstring changes which tool the LLM picks.
- **Checkpointer = memory as database rows.** Kill the server, restart, ask "what were we
  discussing?" — it remembers because the process never held the memory.
- The **summarization node** keeps long chats cheap: facts survive, bulk is deleted.
- Flip mock → live Oxylabs by adding credentials — the provider seam makes it a one-line change.