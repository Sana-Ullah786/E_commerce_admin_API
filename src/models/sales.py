from datetime import datetime

from sqlalchemy import (Boolean, DateTime, Float, ForeignKey, Integer, String,
                        func)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.database import Base

class Sale(Base):
    """
    Model representing a sale transaction.
    """

    __tablename__ = "sales"
    
    sale_id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    product_id: Mapped[int] = mapped_column(Integer, ForeignKey('products.product_id'), nullable=False)
    quantity_sold: Mapped[int] = mapped_column(Integer, nullable=False)
    revenue: Mapped[float] = mapped_column(Float, nullable=False)
    region: Mapped[str] = mapped_column(String(128), nullable=False)
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    # Relationship with Product
    product = relationship("Product", back_populates="sales")