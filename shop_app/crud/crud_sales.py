from sqlalchemy.orm import Session
from shop_app.schemas import schemas_sales
from shop_app import models
from sqlalchemy import desc, between
from fastapi import WebSocket, WebSocketDisconnect
from datetime import datetime


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


def get_all_order_item(db: Session):
    return db.query(models.OrderItem).order_by(desc(models.OrderItem.created_at)).all()


def get_all_order_item_between_dates(db: Session, start, end):
    start_datetime = datetime.combine(start, datetime.min.time())
    end_datetime = datetime.combine(end, datetime.max.time())
    items = db.query(models.OrderItem).filter(between(models.OrderItem.created_at, start_datetime, end_datetime)
    ).order_by(desc(models.OrderItem.created_at)).all()
    return [{
        "created_at": item.created_at.isoformat(),
        "customer_name": item.order.customer_name,
        "customer_email": item.order.customer_email,
        "attendant": item.order.user.fullname,
        "payment_method": item.order.payment_method,
        "product_name": item.product.product_name,
        "quantity": item.quantity,
        "sales_price": item.sales_price,
        "amount": item.sales_price*item.quantity
        } for item in items]


def get_all_jsonable_order_item(db: Session):
    items = get_all_order_item(db)
    return [{
        "created_at": item.created_at.isoformat(),
        "customer_name": item.order.customer_name,
        "customer_email": item.order.customer_email,
        "attendant": item.order.user.fullname ,
        "payment_method": item.order.payment_method,
        "product_name": item.product.product_name,
        "quantity": item.quantity,
        "sales_price": item.sales_price
    } for item in items]


class WebSocketManager:
    def __init__(self):
        self.active_connections = set()

    def add_connection(self, websocket: WebSocket):
        self.active_connections.add(websocket)

    def remove_connection(self, websocket: WebSocket):
        self.active_connections.discard(websocket)

    async def broadcast(self, db: Session):
        sales = get_all_jsonable_order_item(db)

        for connection in list(self.active_connections):
            try:
                await connection.send_json(sales)
            except (WebSocketDisconnect, RuntimeError) as e:
                print(f"Error sending data: {e}")
                self.remove_connection(connection)
            except Exception as e:
                print(f"Unexpected error while sending data: {e}")
                self.remove_connection(connection)
