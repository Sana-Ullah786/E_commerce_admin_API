from sqlalchemy import Integer, String, DateTime, func, Boolean
from sqlalchemy.orm import relationship, mapped_column, Mapped
from datetime import datetime
from src.models.database import Base

class Merchant(Base):
    """
    Model representing a merchant in the database.
    """

    __tablename__ = "merchants"
    
    merchant_id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(128), unique=True, index=True, nullable=False)
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), onupdate=func.now(), nullable=True)
    
    
    # Relationship with ProductMerchant
    product_merchants = relationship('ProductMerchant', back_populates='merchant')
