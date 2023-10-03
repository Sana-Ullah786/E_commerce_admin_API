from datetime import datetime

from pydantic import BaseModel, Field


class SalesSchema(BaseModel):
    product_id: int = Field(description="ID of the product that was sold")
    quantity_sold: int = Field(ge=1, description="Quantity of the product sold")
    region: str = Field(
        min_length=3, max_length=50, description="Region where the sale took place"
    )
