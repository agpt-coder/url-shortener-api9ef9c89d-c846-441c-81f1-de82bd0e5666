from datetime import datetime
from typing import List, Optional

import prisma
import prisma.models
from pydantic import BaseModel


class UpdateUserProfileResponse(BaseModel):
    """
    Response model after the user has successfully updated their profile information.
    """

    message: str
    updatedFields: List[str]
    updateTime: datetime


async def update_profile(
    name: str,
    email: str,
    bio: Optional[str] = None,
    location: Optional[str] = None,
    website: Optional[str] = None,
) -> UpdateUserProfileResponse:
    """
    Allows users to update their profile information.

    Args:
        name (str): The new name for the user's profile.
        email (str): The new email for the user's profile. Must be a valid email format.
        bio (Optional[str]): A brief bio about the user. Optional.
        location (Optional[str]): The user's updated location. Optional.
        website (Optional[str]): URL to the user's personal website or blog. Optional.

    Returns:
        UpdateUserProfileResponse: Response model after the user has successfully updated their profile information, including
                                   the message indicating success, the fields that were updated, and the timestamp of the update.
    """
    user = await prisma.models.User.prisma().find_unique(where={"email": email})
    if not user:
        raise ValueError("User with this email does not exist.")
    update_data = {}
    updatedFields = []
    if name:
        update_data["name"] = name
        updatedFields.append("name")
    if bio:
        update_data["bio"] = bio
        updatedFields.append("bio")
    if location:
        update_data["location"] = location
        updatedFields.append("location")
    if website:
        update_data["website"] = website
        updatedFields.append("website")
    if update_data:
        await prisma.models.User.prisma().update(
            where={"email": email}, data=update_data
        )
    return UpdateUserProfileResponse(
        message="User profile updated successfully.",
        updatedFields=updatedFields,
        updateTime=datetime.now(),
    )
