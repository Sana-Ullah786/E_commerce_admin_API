from pydantic import BaseModel, Field
from typing import Optional

class ProductSchema(BaseModel):
    name: str = Field(min_length=5, max_length=128)
    description: Optional[str] = Field(min_length=10, max_length=256)
    category_id: int = Field(description="category id")
    price: float = Field()
    is_deleted: Optional[bool]
