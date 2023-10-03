from fastapi import Depends, HTTPException, Path, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from src.dependencies import get_db
from src.endpoints.merchant.router_init import router
from src.models import all_models


@router.get("/id/{merchant_id}", status_code=status.HTTP_200_OK, response_model=None)
async def get_merchant_by_id(
    merchant_id: int = Path(gt=-1), db: Session = Depends(get_db)
) -> JSONResponse:
    # get merchant by id
    merchant = (
        db.query(all_models.Merchant)
        .filter(all_models.Merchant.merchant_id == merchant_id)
        .first()
    )
    if merchant is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Merchant not found",
        )
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"message": "Merchant found", "merchant_name": merchant.name},
    )
