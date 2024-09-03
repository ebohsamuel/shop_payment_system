from sqlalchemy.orm import Session
from shop_app.schemas import schemas_sales
from shop_app import models
from sqlalchemy import desc
from fastapi import WebSocket, WebSocketDisconnect


def create_new_order(db: Session, order_details: schemas_sales.OrderCreate):
    db_order = models.Order(**order_details.model_dump())
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order


def get_order_by_id(db: Session, order_id: int):
    return db.query(models.Order).filter(models.Order.id == order_id).first()


def get_all_oder(db: Session):
    return db.query(models.Order).order_by(desc(models.Order.created_at)).all()


def create_new_order_item(db: Session, order_item_details: schemas_sales.OrderItemCreate):
    db_order_item = models.OrderItem(**order_item_details.model_dump())
    db.add(db_order_item)
    return db_order_item


def get_order_item_by_id(db: Session, order_item_id: int):
    return db.query(models.OrderItem).filter(models.OrderItem.id == order_item_id).first()


def get_all_oder_item(db: Session):
    return db.query(models.OrderItem).order_by(desc(models.OrderItem.created_at)).all()

"""
def update_purchase(db: Session, purchase_details: dict, purchase_id: int):
    db_purchase = get_purchase_by_id(db, purchase_id)
    if purchase_details["date_purchased"]:
        db_purchase.date_purchased = purchase_details["date_purchased"]
    if purchase_details["Quantity"]:
        db_purchase.Quantity = purchase_details["Quantity"]
    if purchase_details["per_cost"]:
        db_purchase.per_cost = purchase_details["per_cost"]
    if purchase_details["total_cost"]:
        db_purchase.total_cost = purchase_details["total_cost"]
    db.commit()
    db.refresh(db_purchase)
    return db_purchase


def get_all_purchase(db: Session):
    purchases = db.query(
        models.ProductPurchaseTracking).order_by(desc(models.ProductPurchaseTracking.date_purchased)).all()
    return [{
        "date_purchased": purchase.date_purchased.isoformat(),
        "product_name": purchase.product_name,
        "product_category_id": purchase.product_category_id,
        "Quantity": purchase.Quantity,
        "per_cost": purchase.per_cost,
        "total_cost": purchase.total_cost,
        "id": purchase.id,
        "created_at": purchase.created_at.isoformat()
    } for purchase in purchases]


class WebSocketManager:
    def __init__(self):
        self.active_connections = set()

    def add_connection(self, websocket: WebSocket):
        self.active_connections.add(websocket)

    def remove_connection(self, websocket: WebSocket):
        self.active_connections.discard(websocket)

    async def broadcast(self, db: Session):
        purchases = get_all_purchase(db)

        for connection in list(self.active_connections):
            try:
                await connection.send_json(purchases)
            except (WebSocketDisconnect, RuntimeError) as e:
                print(f"Error sending data: {e}")
                self.remove_connection(connection)
            except Exception as e:
                print(f"Unexpected error while sending data: {e}")
                self.remove_connection(connection)
"""
