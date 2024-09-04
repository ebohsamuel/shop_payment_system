from pydantic import BaseModel
from datetime import datetime


class OrderData(BaseModel):
    product_name: str
    quantity: int
    price: float


class OrderDatas(BaseModel):
    processedItems: list[OrderData] | None = []


class OrderBase(BaseModel):
    user_id: int
    total_amount: float
    customer_name: str
    customer_email: str
    payment_method: str


class OrderCreate(OrderBase):
    pass


class Order(OrderBase):
    id: int
    created_at: datetime

    class ConfigDict:
        from_attributes = True


class OrderItemBase(BaseModel):
    order_id: int
    product_id: int
    product_category_id: int
    quantity: int
    sales_price: float


class OrderItemCreate(OrderItemBase):
    pass


class OrderItem(OrderItemBase):
    id: int
    created_at: datetime

    class ConfigDict:
        from_attributes = True
