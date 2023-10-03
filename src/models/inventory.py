from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.database import Base


class Inventory(Base):
    """
    Model representing the inventory details for products.
    """

    __tablename__ = "inventory"

    inventory_id: Mapped[int] = mapped_column(
        Integer, primary_key=True, index=True, autoincrement=True
    )
    product_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("products.product_id"), index=True, nullable=False
    )
    current_stock: Mapped[int] = mapped_column(Integer, nullable=False)
    low_stock_threshold: Mapped[int] = mapped_column(Integer, nullable=False)
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), onupdate=func.now(), nullable=True
    )

    # Relationship with Product
    product = relationship("Product", back_populates="inventory")

    # Relationship with InventoryLog
    logs = relationship("InventoryLog", back_populates="inventory")
