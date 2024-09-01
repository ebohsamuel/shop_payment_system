from pydantic import BaseModel
from datetime import datetime


class ProductBase(BaseModel):
    product_name: str
    price: float | None = None
    stock: int
    product_category_id: int


class ProductCreate(ProductBase):
    pass


class Product(ProductBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class ConfigDict:
        from_attributes = True
