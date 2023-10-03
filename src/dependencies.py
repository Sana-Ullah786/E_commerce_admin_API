import os
from typing import Generator

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from src.models.database import SessionLocal

SECRET_KEY = os.getenv("JWT_SECRET_KEY")
ALGORITHM = os.getenv("JWT_ALGORITHM")


bcryp_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_bearer = OAuth2PasswordBearer(tokenUrl="token")


def get_db() -> Generator[Session, None, None]:
    """
    A generator function that yields the database session.
    Yields:
        Session: A database session.
    """
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


def get_current_admin(token: str = Depends(oauth2_bearer)) -> dict:
    """
    Fetches user details for a given JWT token.
    Args:
        token (str): The JWT token to decode and extract user information.
    Returns:
        dict: A dictionary containing user details extracted from the token.
    Raises:
        HTTPException: If the token is invalid or missing user information, it raises a
            401 Unauthorized exception.
    """
    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM],
        )
        username: str = payload.get("sub")
        is_admin: bool = payload.get("is_admin")
        if username is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
            )
        elif not is_admin:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User is not an admin",
            )
        return {"username": username, "is_admin": is_admin}
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
        )


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifies a given plain password against a hashed password.
    Args:
        plain_password (str): The plain text password to be verified.
        hashed_password (str): The hashed password against which verification is performed.
    Returns:
        bool: True if the plain password matches the hashed password; otherwise, False.
    """
    return bcryp_context.verify(plain_password, hashed_password)
