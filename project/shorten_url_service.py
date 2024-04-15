import random
import string
from typing import Optional

import prisma
import prisma.models
from pydantic import BaseModel


class ShortenURLResponse(BaseModel):
    """
    Model for the response after shortening a URL. Provides the shortened URL.
    """

    shortened_url: str


async def _generate_short_url(length: int = 8) -> str:
    """
    Generates a random short alias for the URL.

    Args:
        length (int): The desired length of the short URL. Defaults to 8 characters.

    Returns:
        str: A random string consisting of letters and digits used as the shortened URL.
    """
    characters = string.ascii_letters + string.digits
    short_url = "".join((random.choice(characters) for _ in range(length)))
    return short_url


async def shorten_url(
    long_url: str, custom_alias: Optional[str] = None
) -> ShortenURLResponse:
    """
    Converts a long URL into a shortened URL.

    Args:
        long_url (str): The original URL to be shortened.
        custom_alias (Optional[str]): An optional custom alias provided by the user for the URL.

    Returns:
        ShortenURLResponse: Model for the response after shortening a URL. Provides the shortened URL.
    """
    if custom_alias:
        short_url = custom_alias
    else:
        is_unique = False
        short_url = None
        while not is_unique:
            tmp_short_url = await _generate_short_url()
            existing_url = await prisma.models.Url.prisma().find_unique(
                where={"shortUrl": tmp_short_url}
            )
            if not existing_url:
                is_unique = True
                short_url = tmp_short_url
    await prisma.models.Url.prisma().create(
        data={
            "originalUrl": long_url,
            "shortUrl": short_url,
            "alias": custom_alias,
            "userId": "known-user-id-placeholder",
        }
    )
    shortened_url = ShortenURLResponse(shortened_url=short_url)
    return shortened_url
