from langchain_core.tools import tool
from pydantic import BaseModel, Field

from app.services.oxylabs import OxylabsError, get_oxylabs_client


class AmazonProductInput(BaseModel):
    asin: str = Field(description="10-character Amazon ASIN, e.g. 'B08N5WRWNW'")
    domain: str = Field(default="com", description="Amazon marketplace domain")


@tool("amazon_product_details", args_schema=AmazonProductInput)
async def amazon_product_details_tool(asin: str, domain: str = "com") -> str:
    """
    Get detailed information about a specific Amazon product by ASIN. Use after amazon_search
    to get full specs, bullet points, full review breakdown, pricing, stock status, and sales rank.
    """
    try:
        client = get_oxylabs_client()
        data = await client.product_details(asin=asin, domain=domain)

        results_block = data.get("results", [])
        if not isinstance(results_block, list) or not results_block:
            return f"No product data found for ASIN {asin}."

        content = results_block[0].get("content", {})

        title = content.get("title", "N/A")
        brand = content.get("brand", "N/A")
        asin_val = content.get("asin", asin)
        price = content.get("price", "N/A")
        currency = content.get("currency", "")
        rating = content.get("rating", "N/A")
        reviews_count = content.get("reviews_count", "N/A")
        bullet_points_raw = content.get("bullet_points", [])
        if isinstance(bullet_points_raw, list):
            bullet_points = "\n  - " + "\n  - ".join(bullet_points_raw) if bullet_points_raw else "N/A"
        else:
            bullet_points = str(bullet_points_raw)

        rating_distribution = content.get("rating_stars_distribution", {})
        stock = content.get("stock", "N/A")
        is_prime_eligible = content.get("is_prime_eligible", False)
        sales_rank_list = content.get("sales_rank", [])
        sales_rank = sales_rank_list[0] if sales_rank_list else "N/A"
        categories_list = content.get("category", [])
        categories = ", ".join(str(c) for c in categories_list[:2]) if categories_list else "N/A"
        answered_questions_count = content.get("answered_questions_count", "N/A")
        coupon = content.get("coupon", "")
        deal_type = content.get("deal_type", "")

        price_str = f"{currency}{price}" if currency else str(price)
        prime_str = "Yes" if is_prime_eligible else "No"

        dist_str = ""
        if isinstance(rating_distribution, dict) and rating_distribution:
            parts = [f"{k}★: {v}" for k, v in sorted(rating_distribution.items(), reverse=True)]
            dist_str = " | ".join(parts)

        lines = [
            f"Product Details: {title}",
            f"Brand: {brand}",
            f"ASIN: {asin_val}",
            f"Price: {price_str}",
            f"Rating: {rating} ({reviews_count} reviews)",
            f"Prime Eligible: {prime_str}",
            f"Stock: {stock}",
        ]
        if coupon:
            lines.append(f"Coupon: {coupon}")
        if deal_type:
            lines.append(f"Deal Type: {deal_type}")
        lines.append(f"Sales Rank: {sales_rank}")
        lines.append(f"Categories: {categories}")
        lines.append(f"Answered Questions: {answered_questions_count}")
        if dist_str:
            lines.append(f"Rating Distribution: {dist_str}")
        lines.append(f"\nKey Features:{bullet_points}")

        return "\n".join(lines)

    except (OxylabsError, Exception) as exc:
        return f"Product details failed: {exc}"
