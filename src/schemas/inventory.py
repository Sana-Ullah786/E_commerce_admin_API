from pydantic import BaseModel, Field

class InventorySchema(BaseModel):
    product_id: int = Field(description="ID of the related product")
    current_stock: int = Field(ge=0, description="Current stock of the product")
    low_stock_threshold: int = Field(ge=0, description="Threshold below which stock is considered low")
