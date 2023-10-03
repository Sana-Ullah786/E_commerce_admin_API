from pydantic import BaseModel, Field
from typing import Optional

class CategorySchema(BaseModel):
    name: str = Field(min_length=2, max_length=128, description="Name of the category")
    is_deleted: Optional[bool]
