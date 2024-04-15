from datetime import datetime

import prisma
import prisma.models
from pydantic import BaseModel


class GetOriginalUrlResponse(BaseModel):
    """
    This model represents the response containing the original URL associated with the shortened alias.
    """

    originalUrl: str
    alias: str
    expiration_status: str


async def get_original_url(alias: str) -> GetOriginalUrlResponse:
    """
    Retrieves the original URL based on a shortened alias.

    Args:
        alias (str): The unique alias for the shortened URL.

    Returns:
        GetOriginalUrlResponse: This model represents the response containing the original URL associated with the shortened alias.

    Example:
        result = await get_original_url('abc123')
        if result:
            print(result.originalUrl, result.alias, result.expiration_status)
        else:
            print('URL not found or has expired')
    """
    url_entry = await prisma.models.Url.prisma().find_unique(where={"alias": alias})
    if url_entry:
        if url_entry.expiresAt and url_entry.expiresAt < datetime.now():
            expiration_status = "expired"
        else:
            expiration_status = "active"
        return GetOriginalUrlResponse(
            originalUrl=url_entry.originalUrl,
            alias=url_entry.alias if url_entry.alias else "",
            expiration_status=expiration_status,
        )
    return GetOriginalUrlResponse(
        originalUrl="", alias="", expiration_status="not found or expired"
    )
