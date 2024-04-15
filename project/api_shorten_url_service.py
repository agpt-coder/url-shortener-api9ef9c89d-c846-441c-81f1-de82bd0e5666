from typing import Optional

import prisma
import prisma.models
from pydantic import BaseModel


class ApiShortenUrlResponse(BaseModel):
    """
    Model for the response data from the API endpoint for URL shortening. It returns the original URL, the shortened URL, and the alias.
    """

    original_url: str
    shortened_url: str
    alias: str


async def api_shorten_url(
    original_url: str, custom_alias: Optional[str]
) -> ApiShortenUrlResponse:
    """
    Programmatically create shortened URLs via API.

    Args:
        original_url (str): The original URL to be shortened.
        custom_alias (Optional[str]): An optional custom alias for the shortened URL.

    Returns:
        ApiShortenUrlResponse: Model for the response data from the API endpoint for URL shortening. It returns the original URL, the shortened URL, and the alias.
    """
    short_url_stub = "http://short.url/"
    alias_if_required = custom_alias if custom_alias else "generatedAlias123"
    shortened_url = short_url_stub + alias_if_required
    url_entry = await prisma.models.Url.prisma().create(
        data={
            "originalUrl": original_url,
            "shortUrl": shortened_url,
            "alias": alias_if_required,
            "userId": "UUID-of-the-user",
        }
    )
    return ApiShortenUrlResponse(
        original_url=url_entry.originalUrl,
        shortened_url=url_entry.shortUrl,
        alias=url_entry.alias,
    )
