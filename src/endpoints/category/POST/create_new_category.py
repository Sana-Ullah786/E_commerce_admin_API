from fastapi import HTTPException, status, Depends
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
from src.endpoints.category.router_init import router
from src.models import all_models
from src.schemas.category import CategorySchema
from src.dependencies import get_db


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=None)
async def create_category(category: CategorySchema, db: Session = Depends(get_db)) -> JSONResponse:

    new_category = all_models.Category(
        name=category.name,
    )

    try:
        db.add(new_category)
        db.commit()
        db.refresh(new_category)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error creating category: {e}",
        )

    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content={"message": "Category created successfully", "category_id": new_category.category_id},
    )
