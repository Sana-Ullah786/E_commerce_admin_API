from fastapi import Depends, HTTPException, Path, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from src.dependencies import get_db
from src.endpoints.inventory.router_init import router
from src.models import all_models

@router.get("/", status_code=status.HTTP_200_OK, response_model=None)
async def get_all_inventory(db: Session = Depends(get_db)) ->JSONResponse:
    # get all inventory
    inventory = db.query(all_models.Inventory).all()
    if inventory is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Inventory not found",
        )
    return {
        "status": status.HTTP_200_OK,
        "message": "Inventory found",
        "data": inventory
    }

@router.get("/{product_id}", status_code=status.HTTP_200_OK, response_model=None)
async def get_status_by_product_id(product_id: int = Path(gt=0), db: Session = Depends(get_db)) ->JSONResponse:
    # get inventory by product id
    inventory = db.query(all_models.Inventory).filter(all_models.Inventory.product_id == product_id).first()
    if inventory is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Inventory not found",
        )
    if inventory.current_stock <= inventory.low_stock_threshold:
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={"message": "Inventory found", "inventory_id": inventory.inventory_id, "current_stock": inventory.current_stock, "alert": "INVENTORY IS LOW FOR THIS ITEM"},
        )
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"message": "Inventory found", "inventory_id": inventory.inventory_id, "current_stock": inventory.current_stock},
    )

@router.get("/category/{category_id}", status_code=status.HTTP_200_OK, response_model=None)
async def get_status_by_category(category_id: int = Path(gt=0), db: Session = Depends(get_db)) ->JSONResponse:
     
    # get inventory by category id
    inventory = db.query(all_models.Inventory).join(all_models.Product).filter(all_models.Product.category_id == category_id).all()
    if inventory is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Inventory not found",
        )
    # check if inventory is low
    low_inventory = []
    enough_inventory = []
    for item in inventory:
        if item.current_stock <= item.low_stock_threshold:
            low_inventory.append(item)
        else:
            enough_inventory.append(item)
    return {
        "status": status.HTTP_200_OK,
        "low_inventory_items": low_inventory,
        "good_inventory_items" : enough_inventory
    }

@router.get("/merchant/{merchant_id}", status_code=status.HTTP_200_OK, response_model=None)
async def get_status_by_merchant(merchant_id: int = Path(gt=0), db: Session = Depends(get_db)) ->JSONResponse:

    # get merchant from merchant
    merchant = db.query(all_models.Merchant).filter(all_models.Merchant.merchant_id == merchant_id).first()
    if merchant is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Merchant not found",
        )
    #  get product ids from productmerchat table using merchant_id
    product_ids = db.query(all_models.ProductMerchant).filter(all_models.ProductMerchant.merchant_id == merchant_id).all()
    if product_ids is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product not found",
        )
    
    # get inventory by product ids
    inventory = []
    for item in product_ids:
        inventory.append(db.query(all_models.Inventory).filter(all_models.Inventory.product_id == item.product_id).first())
    if inventory is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Inventory not found",
        )
    # check if inventory is low
    low_inventory = []
    enough_inventory = []
    for item in inventory:
        if item.current_stock <= item.low_stock_threshold:
            low_inventory.append(item)
        else:
            enough_inventory.append(item)
    return {
        "status": status.HTTP_200_OK,
        "low_inventory_items": low_inventory,
        "good_inventory_items" : enough_inventory
    }
         
    
     
