from fastapi import APIRouter

from src.endpoints import auth











router = APIRouter()
router.include_router(auth.router)