from pydantic import BaseModel


class OrderData(BaseModel):
    product_name: str
    quantity: int


class OrderDatas(BaseModel):
    processedItems: list[OrderData] | None = []
