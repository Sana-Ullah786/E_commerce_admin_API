from datetime import datetime

from sqlalchemy import Boolean, DateTime, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.database import Base


class Category(Base):
    """
    Model for categories table in the database.
    """

    __tablename__ = "categories"

    category_id: Mapped[int] = mapped_column(
        Integer(), primary_key=True, index=True, autoincrement=True
    )
    name: Mapped[str] = mapped_column(
        String(128), nullable=False, unique=True, index=True
    )
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), onupdate=func.now(), nullable=True
    )

    # Relationship with Product
    products = relationship("Product", back_populates="category")
