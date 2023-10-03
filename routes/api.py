from fastapi import APIRouter

from src.endpoints import auth, sales, product, category

router = APIRouter()
router.include_router(auth.router)
router.include_router(sales.router)
router.include_router(product.router)
router.include_router(category.router)
