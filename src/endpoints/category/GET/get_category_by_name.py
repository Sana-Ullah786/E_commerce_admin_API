from fastapi import HTTPException, status, Depends
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
from src.endpoints.category.router_init import router
from src.models import all_models
from src.dependencies import get_db


@router.get("/{category_name}", status_code=status.HTTP_200_OK, response_model=None)
async def get_category_by_name(category_name: str, db: Session = Depends(get_db)) ->JSONResponse:
    
        category = db.query(all_models.Category).filter(all_models.Category.name.ilike(category_name)).first()
        if category is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Category not found",
            )
    
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={"message": "Category found", "category_id": category.category_id},
        )
