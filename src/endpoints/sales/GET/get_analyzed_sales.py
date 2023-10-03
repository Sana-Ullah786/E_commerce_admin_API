from datetime import date, timedelta
from typing import Optional

from fastapi import Depends, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy import func
from sqlalchemy.orm import Session

from src.dependencies import get_db
from src.endpoints.sales.router_init import router
from src.models import all_models


@router.get("/analysis/", status_code=status.HTTP_200_OK, response_model=None)
async def analyze_sales(
    period: str,
    product_id: Optional[int] = None,
    category_id: Optional[int] = None,
    merchant_id: Optional[int] = None,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    region: Optional[str] = None,
    db: Session = Depends(get_db),
) -> JSONResponse:
    today = date.today()

    # Determine start_date based on the period
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

    # Begin the query based on filters
    query = db.query(all_models.Sale).filter(all_models.Sale.sales_date >= start_date)

    if end_date:
        query = query.filter(all_models.Sale.sales_date <= end_date)
    if product_id:
        query = query.filter(all_models.Sale.product_id == product_id)
    if category_id:
        product_ids_for_category = [
            product.product_id
            for product in db.query(all_models.Product.product_id)
            .filter(all_models.Product.category_id == category_id)
            .all()
        ]
        query = query.filter(all_models.Sale.product_id.in_(product_ids_for_category))
    if merchant_id:
        product_ids_for_merchant = [
            product_merchant.product_id
            for product_merchant in db.query(all_models.ProductMerchant.product_id)
            .filter(all_models.ProductMerchant.merchant_id == merchant_id)
            .all()
        ]
        query = query.filter(all_models.Sale.product_id.in_(product_ids_for_merchant))
    if region:
        query = query.filter(all_models.Sale.region == region)

    total_sales = query.count()
    total_revenue = query.with_entities(func.sum(all_models.Sale.revenue)).scalar()

    return {
        "period": period,
        "total_sales": total_sales,
        "total_revenue": total_revenue,
    }
