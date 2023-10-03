from fastapi import APIRouter

from src.endpoints import auth, category, inventory, merchant, product, sales

router = APIRouter()
router.include_router(auth.router)
router.include_router(product.router)
router.include_router(category.router)
router.include_router(merchant.router)
router.include_router(inventory.router)
router.include_router(sales.router)
