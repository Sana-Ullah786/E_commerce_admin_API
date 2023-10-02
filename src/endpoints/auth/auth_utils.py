import os
from datetime import datetime, timedelta
from typing import Union
import pytz
from fastapi import status
from jose import jwt
from sqlalchemy import or_, select
from sqlalchemy.orm import Session
from fastapi import HTTPException
from src.dependencies import get_password_hash  
from src.dependencies import verify_password 
from src.models.user import User
from src.schemas.user import UserSchema

SECRET_KEY = os.getenv("JWT_SECRET_KEY")
ALGORITHM = os.getenv("JWT_ALGORITHM")


def create_user(user: UserSchema, db: Session) -> UserSchema:
    """
    Helper function that creates a user based on the parameters provided and returns the user. It also checks if the user already exists. Raises an exception if it does.
    """

    check_user_already_exists(user, db)

    new_user = User()
    new_user.email = user.email
    new_user.username = user.username
    new_user.first_name = user.first_name
    new_user.last_name = user.last_name
    new_user.password = get_password_hash(user.password)
    new_user.is_active = True

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return user


def check_user_already_exists(user: UserSchema, db: Session) -> None:
    """
    Raises an exception is user with the same email or username already exists
    """

    fetched_user = db.scalar(
        select(User).where(
            or_(User.email == user.email, User.username == user.username)
        )
    )
    if fetched_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with the same email or username already exists.",
        )


def authenticate_user(username: str, password: str, db: Session) -> Union[User, bool]:
    """A helper function that authenticates a given username and password"""

    user = db.query(User).filter(User.username == username).first()
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user


def create_token(user: User, expire_time_in_min: int) -> str:
    """
    Takes in a username, id and expire time and returns a JWT token for the user
    """
    encode = {"sub": user.username, "id": user.id, "is_librarian": user.is_librarian}
    expire = datetime.utcnow() + timedelta(minutes=expire_time_in_min)
    encode.update({"exp": expire})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)


def get_jwt_exp(token: str) -> int:
    """
    Returns the expiry for a given token
    """
    decoded = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    return decoded["exp"]