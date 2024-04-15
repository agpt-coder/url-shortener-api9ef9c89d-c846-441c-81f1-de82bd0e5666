from typing import Dict, Optional

import prisma
import prisma.models
from pydantic import BaseModel


class UpdatePreferencesRequest(BaseModel):
    """
    Model for updating user preferences, including alias customization, URL expiration options, and notification settings.
    """

    user_id: str
    alias_customization: bool
    url_expiration: Optional[int] = None
    notification_settings: Dict[str, bool]


class UpdatePreferencesResponse(BaseModel):
    """
    Confirms the updated preferences settings for the user.
    """

    success: bool
    updated_preferences: UpdatePreferencesRequest


async def update_preferences(
    user_id: str,
    alias_customization: bool,
    url_expiration: Optional[int],
    notification_settings: Dict[str, bool],
) -> UpdatePreferencesResponse:
    """
    Users can update their service preferences.

    This function updates the user's preferences in the database based on their inputs and returns a response indicating the success of the operation and the new user preferences.

    Args:
        user_id (str): Unique identifier of the user whose preferences are being updated.
        alias_customization (bool): Flag indicating whether the user wants to customize URL aliases.
        url_expiration (Optional[int]): Preference for default URL expiration settings (in days). Null if URLs should not expire by default.
        notification_settings (Dict[str, bool]): User preferences for receiving notifications about their URLs.

    Returns:
        UpdatePreferencesResponse: Confirms the updated preferences settings for the user.
    """
    await prisma.models.User.prisma().update(
        where={"id": user_id},
        data={
            "aliasCustomization": alias_customization,
            "urlExpiration": url_expiration,
            "notificationSettings": notification_settings,
        },
    )
    return UpdatePreferencesResponse(
        success=True,
        updated_preferences=UpdatePreferencesRequest(
            user_id=user_id,
            alias_customization=alias_customization,
            url_expiration=url_expiration,
            notification_settings=notification_settings,
        ),
    )
