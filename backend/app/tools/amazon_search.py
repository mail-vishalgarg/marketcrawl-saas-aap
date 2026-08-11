from langchain_core.tools import tool
from pydantic import BaseModel, Field

from app.services.oxylabs import OxylabsError, get_oxylabs_client


class AmazonSearchInput(BaseModel):
    query: str = Field(
        description="Product search query, e.g. 'wireless noise cancelling headphones'"
    )
    domain: str = Field(
        default="com",
        description="Amazon marketplace: com, co.uk, de, fr, ca, jp",
    )
    sort_by: str = Field(
        default="featured",
        description="Sort: featured, price_low_to_high, price_high_to_low, average_review, bestsellers",  # noqa: E501
    )


@tool("amazon_search", args_schema=AmazonSearchInput)
async def amazon_search_tool(query: str, domain: str = "com", sort_by: str = "featured") -> str:
    """
    Search Amazon for products matching a query. Use this first to discover relevant products.
    Returns top results with ASIN, title, price, rating, review count, Prime status,
    and sales volume.
    Always call this before getting product details.
    """
    try:
        client = get_oxylabs_client()
        data = await client.search(query=query, domain=domain, sort_by=sort_by)

        # Navigate to the results list
        results_list = []
        results_block = data.get("results", [])
        if isinstance(results_block, list) and results_block:
            first = results_block[0]
            content = first.get("content", {})
            results_list = content.get("results", {}).get("organic", [])
            if not results_list:
                results_list = content.get("results", [])

        if not results_list:
            return "Search returned no results."

        lines = [f"Amazon Search Results for: '{query}'\n"]
        for product in results_list[:10]:
            pos = product.get("pos", "?")
            asin = product.get("asin", "N/A")
            title = product.get("title", "N/A")
            price = product.get("price", "N/A")
            currency = product.get("currency", "")
            rating = product.get("rating", "N/A")
            reviews_count = product.get("reviews_count", "N/A")
            is_prime = product.get("is_prime", False)
            is_amazons_choice = product.get("is_amazons_choice", False)
            sales_volume = product.get("sales_volume", "")
            manufacturer = product.get("manufacturer", "")

            price_str = f"{currency}{price}" if currency else str(price)
            prime_str = "Yes" if is_prime else "No"
            choice_str = " [Amazon's Choice]" if is_amazons_choice else ""

            lines.append(f"{pos}. {title}{choice_str}")
            lines.append(f"   ASIN: {asin}")
            lines.append(f"   Price: {price_str}")
            lines.append(f"   Rating: {rating} | Reviews: {reviews_count} | Prime: {prime_str}")
            if sales_volume:
                lines.append(f"   Sales Volume: {sales_volume}")
            if manufacturer:
                lines.append(f"   Manufacturer: {manufacturer}")
            lines.append("")

        return "\n".join(lines)

    except (OxylabsError, Exception) as exc:
        return f"Search failed: {exc}"
