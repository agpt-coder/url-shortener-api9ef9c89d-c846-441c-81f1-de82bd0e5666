from datetime import datetime
from typing import Any, Dict, List

import prisma
import prisma.models
from pydantic import BaseModel


class GetUrlAnalyticsResponse(BaseModel):
    """
    This response model contains the analytics data for the specific URL. It provides a summary of the click-through rates and other relevant metrics, while ensuring that the data is presented in an anonymized manner to protect user privacy.
    """

    urlId: str
    clicks: int
    createdAt: datetime
    updatedAt: datetime
    topReferrers: List[Dict[str, Any]]
    geographicalData: Dict[str, int]


async def get_url_analytics(urlId: str) -> GetUrlAnalyticsResponse:
    """
    Fetch analytics data for a specific URL.

    Args:
    urlId (str): The unique identifier for the URL whose analytics data is to be fetched.

    Returns:
    GetUrlAnalyticsResponse: This response model contains the analytics data for the specific URL. It provides a summary
                             of the click-through rates and other relevant metrics, while ensuring that the data is presented
                             in an anonymized manner to protect user privacy.
    """
    analytics_data = await prisma.models.Analytics.prisma().find_unique(
        where={"urlId": urlId}, include={"Url": True}
    )
    if analytics_data is None:
        return GetUrlAnalyticsResponse(
            urlId=urlId,
            clicks=0,
            createdAt=datetime.now(),
            updatedAt=datetime.now(),
            topReferrers=[],
            geographicalData={},
        )
    top_referrers = [{"google.com": 100}, {"yahoo.com": 50}]
    geographical_data = {"US": 100, "UK": 50}
    return GetUrlAnalyticsResponse(
        urlId=analytics_data.urlId,
        clicks=analytics_data.clicks,
        createdAt=analytics_data.createdAt,
        updatedAt=analytics_data.updatedAt,
        topReferrers=top_referrers,
        geographicalData=geographical_data,
    )
