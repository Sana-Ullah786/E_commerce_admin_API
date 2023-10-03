from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.database import Base


class ProductMerchant(Base):
    """
    Model representing the association between products and merchants.
    """

    __tablename__ = "product_merchants"

    product_merchant_id: Mapped[int] = mapped_column(
        Integer(), primary_key=True, index=True, autoincrement=True
    )
    product_id: Mapped[int] = mapped_column(
        Integer(), ForeignKey("products.product_id"), nullable=False
    )
    merchant_id: Mapped[int] = mapped_column(
        Integer(), ForeignKey("merchants.merchant_id"), nullable=False
    )
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), onupdate=func.now(), nullable=True
    )

    # Relationship with Product
    product = relationship("Product", backref="product_merchants")

    # Relationship with Merchant
    merchant = relationship("Merchant", back_populates="product_merchants")
