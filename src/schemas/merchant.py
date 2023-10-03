from pydantic import BaseModel, Field

class MerchantSchema(BaseModel):
    name: str = Field(min_length=2, max_length=128, description="Name of the merchant.")