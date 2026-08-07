from langchain_core.tools import tool
from pydantic import BaseModel, Field

from app.services.oxylabs import OxylabsError, get_oxylabs_client


class AmazonBestsellersInput(BaseModel):
    browse_node_id: str = Field(
        description=(
            "Amazon browse node ID for the category, e.g. '172541' for Electronics. "
            "Common node IDs: Electronics=172541, Computers=541966, Headphones=172541, "
            "Cameras=281052, Video Games=468642, Books=283155, Kitchen=284507, "
            "Sports=3375251, Clothing=7141123011, Toys=165793011."
        )
    )
    domain: str = Field(default="com")


@tool("amazon_bestsellers", args_schema=AmazonBestsellersInput)
async def amazon_bestsellers_tool(browse_node_id: str, domain: str = "com") -> str:
    """
    Get the bestselling products in a specific Amazon category by browse node ID.
    Use to understand market leaders. Common node IDs: Electronics=172541, Computers=541966,
    Headphones=172541, Cameras=281052, Video Games=468642, Books=283155, Kitchen=284507,
    Sports=3375251, Clothing=7141123011, Toys=165793011.
    """
    try:
        client = get_oxylabs_client()
        data = await client.bestsellers(browse_node_id=browse_node_id, domain=domain)

        results_block = data.get("results", [])
        if not isinstance(results_block, list) or not results_block:
            return f"No bestseller data found for browse node {browse_node_id}."

        content = results_block[0].get("content", {})
        items = content.get("results", [])
        if not items:
            items = content.get("bestsellers", [])

        if not items:
            return f"No bestseller products found for browse node {browse_node_id}."

        lines = [f"Amazon Bestsellers — Browse Node: {browse_node_id}\n"]
        for product in items[:20]:
            rank = product.get("rank", product.get("pos", "?"))
            asin = product.get("asin", "N/A")
            title = product.get("title", "N/A")
            price = product.get("price", "N/A")
            currency = product.get("currency", "")
            rating = product.get("rating", "N/A")
            is_prime = product.get("is_prime", False)

            price_str = f"{currency}{price}" if currency else str(price)
            prime_str = "Prime" if is_prime else "Non-Prime"

            lines.append(f"#{rank}: {title}")
            lines.append(f"   ASIN: {asin} | Price: {price_str} | Rating: {rating} | {prime_str}")
            lines.append("")

        return "\n".join(lines)

    except (OxylabsError, Exception) as exc:
        return f"Bestsellers lookup failed: {exc}"
