from langchain_core.tools import tool
from pydantic import BaseModel, Field

from app.services.oxylabs import OxylabsError, get_oxylabs_client


class AmazonPricingInput(BaseModel):
    asin: str = Field(description="Amazon ASIN to get all seller prices for")
    domain: str = Field(default="com")


@tool("amazon_pricing", args_schema=AmazonPricingInput)
async def amazon_pricing_tool(asin: str, domain: str = "com") -> str:
    """
    Get all seller prices for a product. Use when comparing price competitiveness —
    shows all sellers, conditions (New/Used), and shipping costs.
    """
    try:
        client = get_oxylabs_client()
        data = await client.pricing(asin=asin, domain=domain)

        results_block = data.get("results", [])
        if not isinstance(results_block, list) or not results_block:
            return f"No pricing data found for ASIN {asin}."

        content = results_block[0].get("content", {})
        title = content.get("title", "N/A")
        asin_val = content.get("asin", asin)

        # Oxylabs amazon_pricing returns sellers as content["pricing"] — a flat list
        sellers = content.get("pricing", [])

        if not sellers:
            return f"Pricing data for ASIN {asin_val}: {title}\nNo seller information available."

        prices = []
        for seller in sellers:
            price = seller.get("price")
            if price is not None:
                try:
                    prices.append(float(price))
                except (ValueError, TypeError):
                    pass

        currency = content.get("currency", "$")
        min_price = min(prices) if prices else None
        max_price = max(prices) if prices else None
        num_sellers = len(sellers)

        lines = [
            f"Pricing for: {title}",
            f"ASIN: {asin_val}",
            f"Total Sellers: {num_sellers}",
        ]
        if min_price is not None and max_price is not None:
            lines.append(f"Price Range: {currency}{min_price:.2f} – {currency}{max_price:.2f}")
        lines.append("\nTop 5 Sellers:")

        for seller in sellers[:5]:
            # Oxylabs field: "seller" (name string), "price", "condition", "price_shipping", "rating_count"
            seller_name = seller.get("seller", seller.get("seller_name", "Unknown Seller"))
            price = seller.get("price", "N/A")
            condition = seller.get("condition", "New")
            shipping_price = seller.get("price_shipping", seller.get("shipping_price", "N/A"))
            rating_count = seller.get("rating_count", "N/A")

            price_str = f"{currency}{price}" if price != "N/A" else "N/A"
            shipping_str = (
                f"{currency}{shipping_price}"
                if shipping_price not in ("N/A", None, 0)
                else "Free shipping"
            )

            lines.append(
                f"  - {seller_name}: {price_str} ({condition}) | Shipping: {shipping_str} | Ratings: {rating_count}"
            )

        return "\n".join(lines)

    except (OxylabsError, Exception) as exc:
        return f"Pricing lookup failed: {exc}"
