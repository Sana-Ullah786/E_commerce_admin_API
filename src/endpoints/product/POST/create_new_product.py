from fastapi import Depends, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from src.dependencies import get_db
from src.endpoints.product.router_init import router
from src.models import all_models
from src.schemas.product import ProductSchema


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=None)
async def create_product(
    product: ProductSchema, db: Session = Depends(get_db)
) -> JSONResponse:
    new_product = all_models.Product(
        name=product.name,
        description=product.description,
        category_id=product.category_id,
        price=product.price,
    )

    try:
        db.add(new_product)
        db.commit()
        db.refresh(new_product)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error creating product: {e}",
        )

    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content={
            "message": "Product created successfully",
            "product_id": new_product.product_id,
        },
    )
