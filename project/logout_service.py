from pydantic import BaseModel


class LogoutResponse(BaseModel):
    """
    Indicates successful logout of the user. The actual process involves invalidation of the user's current token.
    """

    message: str


def logout() -> LogoutResponse:
    """
    End a user's session.

    Args:

    Returns:
    LogoutResponse: Indicates successful logout of the user. The actual process involves invalidation of the user's current token.

    Example:
        logout()
        > <LogoutResponse object with message "Successfully logged out.">
    """
    return LogoutResponse(message="Successfully logged out.")
