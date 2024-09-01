from pydantic import BaseModel
from datetime import date, datetime


class PurchaseBase(BaseModel):
    date_purchased: date
    product_name: str
    product_category_id: int
    Quantity: int
    per_cost: float
    total_cost: float


class PurchaseCreate(PurchaseBase):
    pass


class Purchase(PurchaseBase):
    id: int
    created_at: datetime

    class ConfigDict:
        from_attributes = True
