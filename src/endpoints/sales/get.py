from fastapi import Depends, HTTPException, status

from src.dependencies import get_current_admin
from src.endpoints.sales.router_init import router


@router.get("/", status_code=status.HTTP_200_OK, response_model=None)
async def get_sales() -> dict:
    return {
        "message": "You are authorized to view this page.",
    }
