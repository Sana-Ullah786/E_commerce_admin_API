from fastapi import Depends, HTTPException, Path, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from src.dependencies import get_db
from src.endpoints.category.router_init import router
from src.models import all_models


@router.get("/id/{category_id}", status_code=status.HTTP_200_OK, response_model=None)
async def get_category_by_id(
    category_id: int = Path(gt=-1), db: Session = Depends(get_db)
) -> JSONResponse:
    # get category by id
    category = (
        db.query(all_models.Category)
        .filter(all_models.Category.category_id == category_id)
        .first()
    )
    if category is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Category not found",
        )

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"message": "Category found", "category_name": category.name},
    )
