from sqlalchemy.orm import Session
from shop_app.schemas import schemas_product
from shop_app import models
from fastapi import WebSocket, WebSocketDisconnect


def add_new_product(db: Session, product: schemas_product.ProductCreate):
    db_product = models.Product(**product.model_dump(exclude_none=True))
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


def get_product_by_product_name(db: Session, product_name: str):
    return db.query(models.Product).filter(models.Product.product_name == product_name).first()


def update_product_price(db: Session, price: float | None, product_name: str):
    db_product = get_product_by_product_name(db, product_name)
    if price:
        db_product.price = price
    db.commit()
    db.refresh(db_product)
    return db_product


def get_all_product(db: Session):
    products = db.query(models.Product).all()
    return [{
        "id": product.id,
        "product_name": product.product_name,
        "price": product.price,
        "stock": product.stock,
        "product_category_id": product.product_category_id,
        "created_at": product.created_at.isoformat(),
        "updated_at": product.updated_at.isoformat()
    } for product in products]


class WebSocketManager:
    def __init__(self):
        self.active_connections = set()

    def add_connection(self, websocket: WebSocket):
        self.active_connections.add(websocket)

    def remove_connection(self, websocket: WebSocket):
        self.active_connections.discard(websocket)

    async def broadcast(self, db: Session):
        products = get_all_product(db)

        for connection in list(self.active_connections):
            try:
                await connection.send_json(products)
            except (WebSocketDisconnect, RuntimeError) as e:
                print(f"Error sending data: {e}")
                self.remove_connection(connection)
            except Exception as e:
                print(f"Unexpected error while sending data: {e}")
                self.remove_connection(connection)
