from typing import List
from fastapi import Depends, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from sqlalchemy import func

from src.dependencies import get_db
from src.endpoints.sales.router_init import router
from src.models import all_models

from datetime import date, timedelta
@router.get("/compare_revenue/", status_code=status.HTTP_200_OK, response_model=None)
async def compare_revenue(
        period: str,
        db: Session = Depends(get_db)
) -> JSONResponse:
    today = date.today()

    # Define the start_date based on the given period
    if period == "daily":
        start_date = today
    elif period == "weekly":
        start_date = today - timedelta(days=7)
    elif period == "monthly":
        start_date = today - timedelta(days=30)
    elif period == "annual":
        start_date = today - timedelta(days=365)
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid period. Choose from daily, weekly, monthly, or annual.",
        )

    categories = db.query(all_models.Category).all()
    result = []

    for category in categories:
        product_ids = [product.product_id for product in db.query(all_models.Product.product_id).filter(all_models.Product.category_id == category.category_id).all()]
        
        total_sales = db.query(func.count(all_models.Sale.sale_id)).filter(all_models.Sale.sales_date >= start_date, all_models.Sale.product_id.in_(product_ids)).scalar()
        total_revenue = db.query(func.sum(all_models.Sale.revenue)).filter(all_models.Sale.sales_date >= start_date, all_models.Sale.product_id.in_(product_ids)).scalar()

        result.append({
            "category_name": category.name,
            "category_id": category.category_id,
            "period": period,
            "total_sales": total_sales,
            "total_revenue": total_revenue
        })

    return result