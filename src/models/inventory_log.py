from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.database import Base


class InventoryLog(Base):
    """
    Model representing the log of inventory changes for each product.
    """

    __tablename__ = "inventory_log"

    log_id: Mapped[int] = mapped_column(
        Integer(), primary_key=True, index=True, autoincrement=True
    )
    inventory_id: Mapped[int] = mapped_column(
        Integer(), ForeignKey("inventory.inventory_id"), index=True, nullable=False
    )
    product_id: Mapped[int] = mapped_column(
        Integer(), ForeignKey("products.product_id"), index=True, nullable=False
    )
    previous_stock: Mapped[int] = mapped_column(Integer(), nullable=False, default=0)
    new_stock: Mapped[int] = mapped_column(Integer(), nullable=False)
    total_stock: Mapped[int] = mapped_column(Integer(), nullable=False)
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    # Relationship with Inventory and Product
    inventory = relationship("Inventory", back_populates="logs")
    product = relationship("Product", back_populates="logs")
