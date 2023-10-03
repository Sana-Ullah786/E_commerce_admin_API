from fastapi import Depends, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from src.dependencies import get_db
from src.endpoints.merchant.router_init import router
from src.models import all_models
from src.schemas.merchant import MerchantSchema


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=None)
async def create_merchant(
    merchant: MerchantSchema, db: Session = Depends(get_db)
) -> JSONResponse:
    new_merchant = all_models.Merchant(
        name=merchant.name,
    )

    try:
        db.add(new_merchant)
        db.commit()
        db.refresh(new_merchant)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error creating merchant: {e}",
        )

    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content={
            "message": "Merchant created successfully",
            "merchant_id": new_merchant.merchant_id,
        },
    )
