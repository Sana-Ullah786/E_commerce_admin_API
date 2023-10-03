from fastapi import Depends, HTTPException, Path, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from src.dependencies import get_db
from src.endpoints.inventory.router_init import router
from src.models import all_models

@router.get("/track/{product_id}", status_code=status.HTTP_200_OK, response_model=None)
async def get_track_by_product_id(product_id: int = Path(gt=0), db: Session = Depends(get_db)) ->JSONResponse:
     
    # get all logs from InventoryLogs
    inventory_logs = db.query(all_models.InventoryLog).filter(all_models.InventoryLog.product_id == product_id).all()
     
    if inventory_logs is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Inventory not found",
        )
    
    return {
        "status": status.HTTP_200_OK,
        "message": "Inventory found",
        "data": inventory_logs
    }
