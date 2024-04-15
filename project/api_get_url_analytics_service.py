from typing import Dict, List, Optional

import prisma
import prisma.models
from pydantic import BaseModel


class ApiGetUrlAnalyticsResponse(BaseModel):
    """
    Response model containing the analytics data for a specific URL.
    """

    urlId: str
    clicks: int
    createdAt: str
    mostRecentClick: Optional[str] = None
    geographicData: List[Dict[str, int]]


async def api_get_url_analytics(urlId: str, ApiKey: str) -> ApiGetUrlAnalyticsResponse:
    """
    Retrieve analytics for URLs via API.

    Args:
    urlId (str): The unique identifier of the URL whose analytics are being requested.
    ApiKey (str): The API key provided by the user for authentication.

    Returns:
    ApiGetUrlAnalyticsResponse: Response model containing the analytics data for a specific URL.

    This function first verifies the provided ApiKey against stored ApiKeys for authentication.
    Then, retrieves the analytics data of the specified URL using its urlId and aggregates geographic
    data of clicks. It finally returns this data in the form of an ApiGetUrlAnalyticsResponse object.
    """
    api_key_record = await prisma.models.ApiKey.prisma().find_unique(
        where={"key": ApiKey}
    )
    if api_key_record is None:
        raise ValueError("Invalid API Key")
    analytics_records = await prisma.models.Analytics.prisma().find_many(
        where={"urlId": urlId}, include={"Url": True}
    )
    if not analytics_records:
        raise ValueError("URL ID not found")
    geographic_data: List[Dict[str, int]] = []
    response = ApiGetUrlAnalyticsResponse(
        urlId=urlId,
        clicks=sum((analytics.clicks for analytics in analytics_records)),
        createdAt=str(analytics_records[0].createdAt),
        mostRecentClick=str(
            max((analytics.updatedAt for analytics in analytics_records))
        ),
        geographicData=geographic_data,
    )
    return response
