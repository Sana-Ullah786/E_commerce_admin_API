from sqlalchemy import Integer, String
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
