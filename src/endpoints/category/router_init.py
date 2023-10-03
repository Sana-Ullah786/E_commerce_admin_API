from fastapi import APIRouter, Depends

from src.dependencies import get_current_user

router = APIRouter(
    prefix="/category",
    tags=["category"],
    responses={401: {"user": "Not authorized"}},
    # dependencies=[Depends(get_current_user)],
)
