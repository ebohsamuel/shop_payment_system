from pydantic import BaseModel
from datetime import datetime


class ProductCategoryBase(BaseModel):
    product_name: str
    image_data: bytes


class ProductCategoryCreate(ProductCategoryBase):
    pass


class ProductCategory(ProductCategoryBase):
    id: int
    created_at: datetime

    class ConfigDict:
        from_attributes = True
