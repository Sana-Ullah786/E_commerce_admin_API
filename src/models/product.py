from datetime import datetime

from sqlalchemy import (Boolean, DateTime, Float, ForeignKey, Integer, String,
                        func)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.database import Base


class Product(Base):
    """
    This is the product model that will be used to create the products table
    in the database.
    And will be used to create the product object.
    """

    __tablename__ = "products"

    product_id: Mapped[int] = mapped_column(
        Integer(), primary_key=True, index=True, autoincrement=True
    )
    name: Mapped[str] = mapped_column(String(128), nullable=False, index=True)
    description: Mapped[str] = mapped_column(String(256), nullable=True)
    category_id: Mapped[int] = mapped_column(
        Integer(), ForeignKey("categories.category_id"), index=True, nullable=False
    )
    price: Mapped[float] = mapped_column(Float, nullable=False)
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), onupdate=func.now(), nullable=True
    )

    # Relationship with Category
    category = relationship("Category", back_populates="products")

    # Relationship with Inventory
    inventory = relationship("Inventory", back_populates="product")

    # Relationship with InventoryLog
    logs = relationship("InventoryLog", back_populates="product")
