import httpx
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential

from app.settings import get_settings

OXYLABS_URL = "https://realtime.oxylabs.io/v1/queries"


class OxylabsError(Exception):
    """Raised when the Oxylabs API returns a non-200 response."""


class OxylabsClient:
    def __init__(self, username: str, password: str) -> None:
        self._auth = (username, password)

    @retry(
        retry=retry_if_exception_type(httpx.HTTPStatusError),
        wait=wait_exponential(multiplier=1, min=2, max=30),
        stop=stop_after_attempt(3),
        reraise=True,
    )
    async def _request(self, payload: dict) -> dict:
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                OXYLABS_URL,
                json=payload,
                auth=self._auth,
            )
            if response.status_code != 200:
                response.raise_for_status()
            return response.json()

    async def search(
        self,
        query: str,
        domain: str = "com",
        sort_by: str = "featured",
        pages: int = 1,
    ) -> dict:
        payload = {
            "source": "amazon_search",
            "domain": domain,
            "query": query,
            "sort_by": sort_by,
            "pages": pages,
            "parse": True,
        }
        try:
            return await self._request(payload)
        except httpx.HTTPStatusError as exc:
            raise OxylabsError(f"Oxylabs search failed: {exc}") from exc

    async def product_details(self, asin: str, domain: str = "com") -> dict:
        payload = {
            "source": "amazon_product",
            "domain": domain,
            "query": asin,
            "parse": True,
            "context": [{"key": "autoselect_variant", "value": True}],
        }
        try:
            return await self._request(payload)
        except httpx.HTTPStatusError as exc:
            raise OxylabsError(f"Oxylabs product_details failed: {exc}") from exc

    async def pricing(self, asin: str, domain: str = "com") -> dict:
        payload = {
            "source": "amazon_pricing",
            "domain": domain,
            "query": asin,
            "parse": True,
        }
        try:
            return await self._request(payload)
        except httpx.HTTPStatusError as exc:
            raise OxylabsError(f"Oxylabs pricing failed: {exc}") from exc

    async def bestsellers(self, browse_node_id: str, domain: str = "com") -> dict:
        payload = {
            "source": "amazon_bestsellers",
            "domain": domain,
            "query": browse_node_id,
            "render": "html",
            "parse": True,
        }
        try:
            return await self._request(payload)
        except httpx.HTTPStatusError as exc:
            raise OxylabsError(f"Oxylabs bestsellers failed: {exc}") from exc


def get_oxylabs_client() -> OxylabsClient:
    settings = get_settings()
    return OxylabsClient(
        username=settings.oxylabs_username,
        password=settings.oxylabs_password,
    )
