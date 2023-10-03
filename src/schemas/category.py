from typing import Optional

from pydantic import BaseModel, Field


class CategorySchema(BaseModel):
    name: str = Field(min_length=2, max_length=128, description="Name of the category")
    is_deleted: Optional[bool]
