from fastapi import Depends, HTTPException, status, Path
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from src.dependencies import get_db
from src.endpoints.inventory.router_init import router
from src.models import all_models

@router.put("/{product_id}", status_code=status.HTTP_201_CREATED, response_model=None)
async def update_inventory_by_product_id(product_id: int = Path(ge=0), db: Session = Depends(get_db),  new_stock: int = 0) ->JSONResponse:
    
    if not new_stock:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"New stock is required",
        )
    inventory = db.query(all_models.Inventory).filter(all_models.Inventory.product_id == product_id).first()
    if not inventory:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Inventory with id {product_id} not found",
        )
    
    try:
        old_stock = inventory.current_stock
        inventory.current_stock += new_stock
        db.commit()
        db.refresh(inventory)
        # insert inventory log
        new_inventory_log = all_models.InventoryLog (
            inventory_id = inventory.inventory_id,
            product_id = inventory.product_id,
            previous_stock = old_stock,
            new_stock = new_stock,
            total_stock = new_stock + old_stock
        )
        db.add(new_inventory_log)
        db.commit()
        db.refresh(new_inventory_log)

    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error updating inventory: {e}",
        )
    
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content={"message": "Inventory updated successfully", "inventory_id": inventory.inventory_id},
    )
