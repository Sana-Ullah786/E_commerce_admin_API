from fastapi import Depends, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from src.dependencies import get_db
from src.endpoints.merchant.router_init import router
from src.models import all_models


@router.get("/{merchant_name}", status_code=status.HTTP_200_OK, response_model=None)
async def get_merchant_by_name(
    merchant_name: str, db: Session = Depends(get_db)
) -> JSONResponse:
    # get merchant by name case insensitive
    merchant = (
        db.query(all_models.Merchant)
        .filter(all_models.Merchant.name.ilike(merchant_name))
        .first()
    )
    if merchant is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Merchant not found",
        )
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"message": "Merchant found", "merchant_id": merchant.merchant_id},
    )
