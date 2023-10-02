from fastapi import APIRouter

from src.endpoints import auth, sales

router = APIRouter()
router.include_router(auth.router)
router.include_router(sales.router)
