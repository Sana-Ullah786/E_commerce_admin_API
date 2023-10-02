import logging
import os
from typing import Generator, Tuple

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy import select
from sqlalchemy.orm import Session

# from src.exceptions import custom_exception
from src.models.database import SessionLocal
# from src.models.user import User

SECRET_KEY = os.getenv("JWT_SECRET_KEY")
ALGORITHM = os.getenv("JWT_ALGORITHM")


bcryp_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_bearer = OAuth2PasswordBearer(tokenUrl="token")



def get_db() -> Generator[Session, None, None]:
    """
    A generetor function that yields the DB session
    """
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


def get_current_user(token: str = Depends(oauth2_bearer)) -> dict:
    """
    Fetches user details for a given token.
    To be used as a dependency by authenticated routes for users
    """
    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM],
        )
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
        )


def get_password_hash(password: str) -> str:
    """A helper function that hashes a given password"""

    return bcryp_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """A helper function that verifies a given password against a hashed password"""

    return bcryp_context.verify(plain_password, hashed_password)