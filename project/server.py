import logging
from contextlib import asynccontextmanager
from typing import Dict, Optional

import project.api_get_url_analytics_service
import project.api_shorten_url_service
import project.get_original_url_service
import project.get_url_analytics_service
import project.login_service
import project.logout_service
import project.manage_api_keys_service
import project.register_service
import project.shorten_url_service
import project.update_preferences_service
import project.update_profile_service
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.responses import Response
from prisma import Prisma

logger = logging.getLogger(__name__)

db_client = Prisma(auto_register=True)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await db_client.connect()
    yield
    await db_client.disconnect()


app = FastAPI(
    title="URL Shortener API",
    lifespan=lifespan,
    description="Based on the exchange, the task involves creating a URL shortening service with specified functional features and operational considerations. The service will need to accept a long URL as input, generate a unique, concise alias that is both easy to remember and includes a mix of letters and numbers, and store this alias alongside the original URL. Given the user's preferences, the alias format should aim for readability and uniqueness, incorporating strategies discussed such as appending numerical identifiers, using slugs derived from the original URL, or including timestamps for guaranteed uniqueness.\n\nThe shortened URLs can be either permanent or expire after a certain period, depending on the service provider's policy, emphasizing the need for flexibility in the system's design to accommodate different user preferences. Performance and scalability requirements suggest the system should be capable of handling a significant user load, including thousands of concurrent requests, with efficient database performance to ensure quick retrieval and storage of URL mappings.\n\nBest practices for generating unique URL aliases and securely storing URL mappings in a database have been highlighted. These include using strong encryption, implementing proper access control, using hashing for sensitive mappings, and regular security audits. The tech stack selected for this project involves Python and FastAPI for the API framework, PostgreSQL for the database, and Prisma as the ORM, which supports these requirements.\n\nAn example of redirecting shortened URLs to their original URLs using FastAPI has been provided, demonstrating a basic implementation of the URL redirect feature. The system must also include endpoints for creating shortened URLs and retrieving the original URLs based on the shortened alias. Integrating these elements will meet the project's goals and ensure a scalable, secure, and user-friendly URL shortening service.",
)


@app.get(
    "/analytics/{urlId}",
    response_model=project.get_url_analytics_service.GetUrlAnalyticsResponse,
)
async def api_get_get_url_analytics(
    urlId: str,
) -> project.get_url_analytics_service.GetUrlAnalyticsResponse | Response:
    """
    Fetch analytics data for a specific URL.
    """
    try:
        res = await project.get_url_analytics_service.get_url_analytics(urlId)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.get(
    "/url/{alias}",
    response_model=project.get_original_url_service.GetOriginalUrlResponse,
)
async def api_get_get_original_url(
    alias: str,
) -> project.get_original_url_service.GetOriginalUrlResponse | Response:
    """
    Retrieves the original URL based on a shortened alias.
    """
    try:
        res = await project.get_original_url_service.get_original_url(alias)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.get(
    "/user/api-keys",
    response_model=project.manage_api_keys_service.ManageApiKeysResponse,
)
async def api_get_manage_api_keys() -> project.manage_api_keys_service.ManageApiKeysResponse | Response:
    """
    Retrieve and manage API keys for the user.
    """
    try:
        res = await project.manage_api_keys_service.manage_api_keys()
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.post(
    "/auth/register", response_model=project.register_service.UserRegistrationResponse
)
async def api_post_register(
    email: str, password: str, confirmPassword: str, agreeToPrivacyPolicy: bool
) -> project.register_service.UserRegistrationResponse | Response:
    """
    Register a new user.
    """
    try:
        res = await project.register_service.register(
            email, password, confirmPassword, agreeToPrivacyPolicy
        )
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.get(
    "/api/analytics/{urlId}",
    response_model=project.api_get_url_analytics_service.ApiGetUrlAnalyticsResponse,
)
async def api_get_api_get_url_analytics(
    urlId: str, ApiKey: str
) -> project.api_get_url_analytics_service.ApiGetUrlAnalyticsResponse | Response:
    """
    Retrieve analytics for URLs via API.
    """
    try:
        res = await project.api_get_url_analytics_service.api_get_url_analytics(
            urlId, ApiKey
        )
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.post("/auth/logout", response_model=project.logout_service.LogoutResponse)
async def api_post_logout() -> project.logout_service.LogoutResponse | Response:
    """
    End a user's session.
    """
    try:
        res = project.logout_service.logout()
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.post(
    "/api/url/shorten",
    response_model=project.api_shorten_url_service.ApiShortenUrlResponse,
)
async def api_post_api_shorten_url(
    original_url: str, custom_alias: Optional[str]
) -> project.api_shorten_url_service.ApiShortenUrlResponse | Response:
    """
    Programmatically create shortened URLs via API.
    """
    try:
        res = await project.api_shorten_url_service.api_shorten_url(
            original_url, custom_alias
        )
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.post("/url/shorten", response_model=project.shorten_url_service.ShortenURLResponse)
async def api_post_shorten_url(
    long_url: str, custom_alias: Optional[str]
) -> project.shorten_url_service.ShortenURLResponse | Response:
    """
    Converts a long URL into a shortened URL.
    """
    try:
        res = await project.shorten_url_service.shorten_url(long_url, custom_alias)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.post("/auth/login", response_model=project.login_service.LoginResponse)
async def api_post_login(
    email: str, password: str
) -> project.login_service.LoginResponse | Response:
    """
    Authenticate a user and return a JWT.
    """
    try:
        res = await project.login_service.login(email, password)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.put(
    "/user/preferences",
    response_model=project.update_preferences_service.UpdatePreferencesResponse,
)
async def api_put_update_preferences(
    user_id: str,
    alias_customization: bool,
    url_expiration: Optional[int],
    notification_settings: Dict[str, bool],
) -> project.update_preferences_service.UpdatePreferencesResponse | Response:
    """
    Users can update their service preferences.
    """
    try:
        res = await project.update_preferences_service.update_preferences(
            user_id, alias_customization, url_expiration, notification_settings
        )
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.put(
    "/user/profile",
    response_model=project.update_profile_service.UpdateUserProfileResponse,
)
async def api_put_update_profile(
    name: str,
    email: str,
    bio: Optional[str],
    location: Optional[str],
    website: Optional[str],
) -> project.update_profile_service.UpdateUserProfileResponse | Response:
    """
    Allows users to update their profile information.
    """
    try:
        res = await project.update_profile_service.update_profile(
            name, email, bio, location, website
        )
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )
