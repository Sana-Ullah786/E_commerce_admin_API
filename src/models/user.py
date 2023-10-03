from datetime import datetime

from sqlalchemy import Boolean, DateTime, Integer, String, func
from sqlalchemy.orm import Mapped, deferred, mapped_column

from src.models.database import Base


class User(Base):
    """
    This is the user model that will be used to create the users table
    in the database.
    And will be used to create the user object
    """

    __tablename__ = "user"
    id: Mapped[int] = mapped_column(Integer(), primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String(32), unique=True, index=True)
    password: Mapped[str] = deferred(
        mapped_column(String(256), unique=True, index=True)
    )
    is_admin: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), onupdate=func.now(), nullable=True
    )
