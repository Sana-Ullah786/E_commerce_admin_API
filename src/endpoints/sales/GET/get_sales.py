from fastapi import Depends, HTTPException, Path, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from src.dependencies import get_db
from src.endpoints.sales.router_init import router
from src.models import all_models


@router.get("/", response_model=None)
async def get_all_sales(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
) -> JSONResponse:
    sales = db.query(all_models.Sale).offset(skip).limit(limit).all()
    return {"status": status.HTTP_200_OK, "message": "Sales found", "data": sales}
