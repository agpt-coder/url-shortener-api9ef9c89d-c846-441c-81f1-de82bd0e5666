from datetime import datetime
from typing import List

import prisma
import prisma.models
from pydantic import BaseModel


class ApiKeyDetails(BaseModel):
    """
    Details of an individual API key owned by the user.
    """

    key: str
    createdAt: datetime
    permissions: List[str]


class ManageApiKeysResponse(BaseModel):
    """
    Provides a detailed view of the user's API keys including creation dates and any relevant metadata.
    """

    api_keys: List[ApiKeyDetails]


async def manage_api_keys() -> ManageApiKeysResponse:
    """
    Retrieve and manage API keys for the user.

    This function's purpose is to provide a user-friendly interface for managing API keys
    including retrieval of existing keys, and potentially creating, updating, or deleting keys
    in the context of an URL shortening service. This function assumes the user's identity
    is verified and their unique user ID is available in the session or via API tokens.

    Returns:
        ManageApiKeysResponse: Provides a detailed view of the user's API keys including
        creation dates and any relevant metadata such as permissions.
    """
    user_id = "user-id-placeholder"
    api_keys = await prisma.models.ApiKey.prisma().find_many(where={"userId": user_id})
    api_keys_details = [
        ApiKeyDetails(
            key=api_key.key, createdAt=api_key.createdAt, permissions=["read", "write"]
        )
        for api_key in api_keys
    ]
    return ManageApiKeysResponse(api_keys=api_keys_details)
