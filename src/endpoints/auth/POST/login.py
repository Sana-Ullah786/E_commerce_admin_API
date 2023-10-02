import os

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from src.dependencies import get_db
from src.endpoints.auth.auth_utils import authenticate_user, create_token
from src.endpoints.auth.router_init import router
from src.schemas.user import UserSchemaToken

EXPIRE_TIME_IN_MINUTES = int(os.getenv("JWT_EXPIRE_TIME_IN_MINUTES"))


@router.post("/token", status_code=status.HTTP_200_OK, response_model=None)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
) -> dict:
    """
    Logs in a user using username and password and returns the access token and the user object.
    Args:
        form_data (OAuth2PasswordRequestForm): A Pydantic model representing the username and password
            submitted in the request form.
        db (Session): The database session to query for user authentication.
    Returns:
        dict: A dictionary containing the access token and additional information.
    Raises:
        HTTPException: If the provided username and password are invalid, it raises a
            401 Unauthorized exception with an error message.
    """
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
        )
    access_token = create_token(user, EXPIRE_TIME_IN_MINUTES)
    user = UserSchemaToken(access_token=access_token)
    return HTTPException(
        status_code=status.HTTP_200_OK,
        detail="Login successful",
        headers={"Authorization": f"Bearer {access_token}"},
    )
