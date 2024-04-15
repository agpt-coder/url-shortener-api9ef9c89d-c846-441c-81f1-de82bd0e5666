from datetime import datetime, timedelta

import prisma
import prisma.models
from jose import jwt
from passlib.context import CryptContext
from pydantic import BaseModel


class LoginResponse(BaseModel):
    """
    The response model for a successful login action. It includes a JWT token that will be used for authenticating subsequent requests.
    """

    jwt_token: str


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


async def authenticate_user(email: str, password: str) -> prisma.models.User | None:
    """
    Authenticates a user by verifying the given email and password.

    Args:
        email (str): The email of the user attempting to login.
        password (str): The password of the user attempting to login.

    Returns:
        Optional[prisma.models.User]: The authenticated user object or None if authentication fails.
    """
    user = await prisma.models.User.prisma().find_unique(where={"email": email})
    if user and pwd_context.verify(password, user.password):
        return user
    return None


def create_access_token(data: dict) -> str:
    """
    Generates a JWT token for authenticated users.

    Args:
        data (dict): Data to encode in the JWT token.

    Returns:
        str: A JWT token representing the encoded data.
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=30)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, "SECRET_KEY", algorithm="HS256")
    return encoded_jwt


async def login(email: str, password: str) -> LoginResponse:
    """
    Authenticate a user and return a JWT.

    Args:
    email (str): The email address of the user trying to log in. This field is used to identify the user in the database.
    password (str): The password for the user attempting to log in. This will be verified against the hashed password stored in the database.

    Returns:
    LoginResponse: The response model for a successful login action. It includes a JWT token that will be used for authenticating subsequent requests.
    """
    user = await authenticate_user(email, password)
    if not user:
        raise Exception("Incorrect email or password")
    access_token = create_access_token(data={"sub": user.email})
    return LoginResponse(jwt_token=access_token)
