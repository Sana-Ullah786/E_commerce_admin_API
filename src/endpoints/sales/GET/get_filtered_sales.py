from datetime import date
from typing import Optional

from fastapi import Depends, HTTPException, Path, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from src.dependencies import get_db
from src.endpoints.sales.router_init import router
from src.models import all_models


@router.get("/by_product", response_model=None)
async def get_sales_by_product(
    product_id: int,
    skip: int = 0,
    limit: int = 100,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    region: Optional[str] = None,
    db: Session = Depends(get_db),
) -> JSONResponse:
    """
    Fetch sales data by a specific product.

    Args:
    - product_id: ID of the product to fetch sales for.
    """
    query = db.query(all_models.Sale).filter(all_models.Sale.product_id == product_id)

    if start_date:
        query = query.filter(all_models.Sale.sales_date >= start_date)
    if end_date:
        query = query.filter(all_models.Sale.sales_date <= end_date)
    if region:
        query = query.filter(all_models.Sale.region == region)

    sales = query.offset(skip).limit(limit).all()

    return {
        "status": status.HTTP_200_OK,
        "message": f"Sales found for product {product_id}",
        "data": sales,
    }


@router.get("/by_category", response_model=None)
async def get_sales_by_category(
    category_id: int,
    skip: int = 0,
    limit: int = 100,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    region: Optional[str] = None,
    db: Session = Depends(get_db),
) -> JSONResponse:
    """
    Fetch sales data by a specific category.

    Args:
    - category_id: ID of the category to fetch sales for.
    """
    product_ids = [
        product.product_id
        for product in db.query(all_models.Product.product_id)
        .filter(all_models.Product.category_id == category_id)
        .all()
    ]

    query = db.query(all_models.Sale).filter(
        all_models.Sale.product_id.in_(product_ids)
    )

    if start_date:
        query = query.filter(all_models.Sale.sales_date >= start_date)
    if end_date:
        query = query.filter(all_models.Sale.sales_date <= end_date)
    if region:
        query = query.filter(all_models.Sale.region == region)

    sales = query.offset(skip).limit(limit).all()

    return {
        "status": status.HTTP_200_OK,
        "message": f"Sales found for category {category_id}",
        "data": sales,
    }


@router.get("/by_merchant", response_model=None)
async def get_sales_by_merchant(
    merchant_id: int,
    skip: int = 0,
    limit: int = 100,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    region: Optional[str] = None,
    db: Session = Depends(get_db),
) -> JSONResponse:
    """
    Fetch sales data by a specific merchant.

    Args:
    - merchant_id: ID of the merchant to fetch sales for.
    """
    product_ids = [
        product_merchant.product_id
        for product_merchant in db.query(all_models.ProductMerchant.product_id)
        .filter(all_models.ProductMerchant.merchant_id == merchant_id)
        .all()
    ]

    query = db.query(all_models.Sale).filter(
        all_models.Sale.product_id.in_(product_ids)
    )

    if start_date:
        query = query.filter(all_models.Sale.sales_date >= start_date)
    if end_date:
        query = query.filter(all_models.Sale.sales_date <= end_date)
    if region:
        query = query.filter(all_models.Sale.region == region)

    sales = query.offset(skip).limit(limit).all()

    return {
        "status": status.HTTP_200_OK,
        "message": f"Sales found for merchant {merchant_id}",
        "data": sales,
    }
