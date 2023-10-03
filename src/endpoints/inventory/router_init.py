from fastapi import APIRouter, Depends

from src.dependencies import get_current_admin

router = APIRouter(
    prefix="/inventory",
    tags=["inventory"],
    responses={401: {"user": "Not authorized"}},
    # dependencies=[Depends(get_current_admin)],
)
