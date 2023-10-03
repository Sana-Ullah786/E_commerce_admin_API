from fastapi import Depends, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from src.dependencies import get_db
from src.endpoints.sales.router_init import router
from src.models import all_models
from src.schemas.sales import SalesSchema


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=None)
async def create_sale(sale: SalesSchema, db: Session = Depends(get_db)) -> JSONResponse:
    # get product
    product = (
        db.query(all_models.Product)
        .filter(all_models.Product.product_id == sale.product_id)
        .first()
    )
    if product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product not found",
        )

    # get inventory
    inventory = (
        db.query(all_models.Inventory)
        .filter(all_models.Inventory.product_id == sale.product_id)
        .first()
    )
    if inventory is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Inventory not found",
        )

    # check if there is enough stock
    if inventory.current_stock < sale.quantity_sold:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Insufficient stock",
        )

    # create new sale
    new_sale = all_models.Sale(
        product_id=sale.product_id,
        quantity_sold=sale.quantity_sold,
        region=sale.region,
        revenue=product.price * sale.quantity_sold,
    )

    try:
        db.add(new_sale)
        db.commit()
        db.refresh(new_sale)
        # update inventory
        inventory.current_stock = inventory.current_stock - sale.quantity_sold
        db.commit()
        db.refresh(inventory)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error creating sale: {e}",
        )

    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content={"message": "Sale created successfully", "sale_id": new_sale.sale_id},
    )
