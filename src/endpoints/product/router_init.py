from fastapi import APIRouter, Depends

from src.dependencies import get_current_user

router = APIRouter(
    prefix="/product",
    tags=["product"],
    responses={401: {"user": "Not authorized"}},
    # dependencies=[Depends(get_current_user)],
)
