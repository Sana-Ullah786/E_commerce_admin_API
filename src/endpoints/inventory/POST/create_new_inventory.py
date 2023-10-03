from fastapi import Depends, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from src.dependencies import get_db
from src.endpoints.inventory.router_init import router
from src.models import all_models
from src.schemas.inventory import InventorySchema


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=None)
async def create_inventory(
    inventory: InventorySchema, db: Session = Depends(get_db)
) -> JSONResponse:
    new_inventory = all_models.Inventory(
        product_id=inventory.product_id,
        current_stock=inventory.current_stock,
        low_stock_threshold=inventory.low_stock_threshold,
    )

    try:
        db.add(new_inventory)
        db.commit()
        db.refresh(new_inventory)
        # insert inventory log
        new_inventory_log = all_models.InventoryLog(
            inventory_id=new_inventory.inventory_id,
            product_id=inventory.product_id,
            previous_stock=0,
            new_stock=inventory.current_stock,
            total_stock=inventory.current_stock,
        )
        db.add(new_inventory_log)
        db.commit()
        db.refresh(new_inventory_log)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error creating inventory: {e}",
        )

    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content={
            "message": "Inventory created successfully",
            "inventory_id": new_inventory.inventory_id,
        },
    )
