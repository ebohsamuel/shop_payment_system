from sqlalchemy.orm import Session
from shop_app.schemas import schema_product_category
from shop_app import models


def add_new_product_category(db: Session, product_category: schema_product_category.ProductCategoryCreate):
    db_product_category = models.ProductCategory(
        product_name=product_category.product_name,
        image_data=product_category.image_data
    )
    db.add(db_product_category)
    db.commit()
    db.refresh(db_product_category)
    return db_product_category


def get_product_category_by_id(db: Session, product_category_id: int):
    return db.query(models.ProductCategory).filter(models.ProductCategory.id == product_category_id).first()


def get_product_category_by_product_name(db: Session, product_name: str):
    return db.query(models.ProductCategory).filter(models.ProductCategory.product_name == product_name).first()


def update_product_category(db: Session, product_category_details: dict, product_category_id: int):
    db_product_category = get_product_category_by_id(db, product_category_id)
    if product_category_details["product_name"]:
        db_product_category.product_name = product_category_details["product_name"]
    if product_category_details["image_data"]:
        db_product_category.image_data = product_category_details["image_data"]
    db.commit()
    db.refresh(db_product_category)
    return db_product_category


def get_all_product_category(db: Session):
    return db.query(models.ProductCategory).all()
