from fastapi import APIRouter, Depends

from src.dependencies import get_current_admin

router = APIRouter(
    prefix="/merchant",
    tags=["merchant"],
    responses={401: {"user": "Not authorized"}},
    dependencies=[Depends(get_current_admin)],
)
