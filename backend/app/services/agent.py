from fastapi import HTTPException
from langchain.agents import create_agent
from langchain.agents.middleware import ModelRetryMiddleware, ToolRetryMiddleware
from langchain_openai import ChatOpenAI

from app.settings import get_settings
from app.tools.amazon_bestsellers import amazon_bestsellers_tool
from app.tools.amazon_pricing import amazon_pricing_tool
from app.tools.amazon_product import amazon_product_details_tool
from app.tools.amazon_search import amazon_search_tool

SYSTEM_PROMPT = """You are an elite Amazon market intelligence analyst. Your mission is to provide \
data-driven competitive analysis based on real-time Amazon data.

ANALYSIS STRATEGY:
1. Start with amazon_search to map the product landscape (always)
2. Get amazon_product_details for the top 3-5 most relevant results
3. Use amazon_pricing when the question is about price competitiveness or best deals
4. Use amazon_bestsellers when the question involves market leaders or top sellers
5. For brand comparisons, search for each brand separately

QUALITY STANDARDS:
- Only recommend products with meaningful review counts (>50 reviews minimum)
- Always cite ASIN, current price, and star rating for every product mentioned
- Never fabricate data — if a tool fails, note it and continue with available data
- Compare products on dimensions the user cares about (price/perf, durability, etc.)
- Identify the value winner at each price tier when relevant

MANDATORY OUTPUT FORMAT:
## Market Overview
[Price range in this category, number of major players, key trends]

## Top Contenders
[Markdown table: | Product | ASIN | Price | Rating | Reviews | Prime |]

## Product Deep Dive
[2–4 sentences on each shortlisted product's strengths/weaknesses]

## Value Analysis
[Budget pick / Best overall / Premium pick — with clear reasoning]

## Bottom Line
[Direct 1–2 sentence answer to the user's exact question]

Be concise, analytical, and data-driven. Users rely on your analysis for purchase decisions."""


def build_agent():  # type: ignore[return]
    settings = get_settings()
    llm = ChatOpenAI(
        model="gpt-4o",
        temperature=0,
        api_key=settings.openai_api_key,  # type: ignore[arg-type]
        max_tokens=4096,
    )
    tools = [
        amazon_search_tool,
        amazon_product_details_tool,
        amazon_pricing_tool,
        amazon_bestsellers_tool,
    ]
    return create_agent(
        model=llm,
        tools=tools,
        system_prompt=SYSTEM_PROMPT,
        middleware=[
            ModelRetryMiddleware(max_retries=3),
            ToolRetryMiddleware(max_retries=2),
        ],
    )


async def run_analysis(question: str, marketplace: str = "com") -> dict:
    try:
        agent = build_agent()
        result = await agent.ainvoke(
            {"messages": [{"role": "user", "content": question}]}
        )
        # result["messages"] is the full conversation; the last entry is the AI response
        messages = result.get("messages", [])
        last_msg = messages[-1] if messages else None
        analysis = (
            last_msg.content
            if last_msg is not None and hasattr(last_msg, "content")
            else str(result)
        )
        return {"analysis": analysis, "question": question, "marketplace": marketplace}
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
