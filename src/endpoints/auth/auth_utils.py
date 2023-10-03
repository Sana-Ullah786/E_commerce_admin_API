import os
from datetime import datetime, timedelta
from typing import Union

from jose import jwt
from sqlalchemy.orm import Session

from src.dependencies import verify_password
from src.models.user import User

SECRET_KEY = os.getenv("JWT_SECRET_KEY")
ALGORITHM = os.getenv("JWT_ALGORITHM")


def authenticate_user(username: str, password: str, db: Session) -> Union[User, bool]:
    """
    Authenticates a user based on their username and password.
    Args:
        username (str): The username of the user to authenticate.
        password (str): The password provided by the user.
        db (Session): The database session to query for user information.
    Returns:
        Union[User, bool]: Returns the authenticated User object if successful, or False if authentication fails.
    """
    user = db.query(User).filter(User.username == username).first()
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user


def create_token(user: User, expire_time_in_min: int) -> str:
    """
    Creates a JSON Web Token (JWT) for a user.
    Args:
        user (User): The User object for whom the token is created.
        expire_time_in_min (int): The expiration time of the token in minutes.
    Returns:
        str: The JWT token as a string.
    """
    encode = {"sub": user.username, "id": user.id, "is_admin": user.is_admin}
    expire = datetime.utcnow() + timedelta(minutes=expire_time_in_min)
    encode.update({"exp": expire})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)


def get_jwt_exp(token: str) -> int:
    """
    Gets the expiry time for a given JWT token.
    Args:
        token (str): The JWT token from which to extract the expiry time.
    Returns:
        int: The expiration time of the token as a Unix timestamp (UTC).
    """
    decoded = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    return decoded["exp"]
