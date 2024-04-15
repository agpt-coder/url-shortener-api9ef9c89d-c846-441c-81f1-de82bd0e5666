import prisma
import prisma.models
from passlib.context import CryptContext
from pydantic import BaseModel


class UserRegistrationResponse(BaseModel):
    """
    Response model for the registration endpoint providing feedback about the registration outcome, including success status and any user-specific messages or identifiers required for further interaction with the API.
    """

    success: bool
    userId: str
    message: str


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


async def register(
    email: str, password: str, confirmPassword: str, agreeToPrivacyPolicy: bool
) -> UserRegistrationResponse:
    """
    Register a new user.

    Args:
    email (str): The email address of the user, used as a unique identifier and for communications.
    password (str): A strong password for account security. Will be hashed and not stored directly.
    confirmPassword (str): A repeat of the password to confirm the user correctly typed what they intended.
    agreeToPrivacyPolicy (bool): Flag if the user has agreed to the privacy policy, in compliance with GDPR.

    Returns:
    UserRegistrationResponse: Response model for the registration endpoint providing feedback about the registration outcome, including success status and any user-specific messages or identifiers required for further interaction with the API.
    """
    if not agreeToPrivacyPolicy:
        return UserRegistrationResponse(
            success=False, userId="", message="You must agree to the privacy policy."
        )
    if password != confirmPassword:
        return UserRegistrationResponse(
            success=False, userId="", message="Passwords do not match."
        )
    hashed_password = pwd_context.hash(password)
    try:
        user = await prisma.models.User.prisma().create(
            data={"email": email, "password": hashed_password}
        )
        return UserRegistrationResponse(
            success=True, userId=user.id, message="User registered successfully."
        )
    except Exception as e:
        return UserRegistrationResponse(
            success=False, userId="", message=f"Failed to register user: {str(e)}"
        )
