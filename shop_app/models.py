from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Date, Float, DateTime, LargeBinary
from sqlalchemy.orm import relationship
from datetime import datetime, timezone


from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String(255), unique=True, index=True)
    hashed_password = Column(String)
    fullname = Column(String)
    is_active = Column(Boolean, default=False)
    is_admin = Column(Boolean)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc).replace(microsecond=0))
    updated_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc).replace(microsecond=0),
        onupdate=lambda: datetime.now(timezone.utc).replace(microsecond=0)
    )

    orders = relationship("Order", back_populates="user")


class ProductCategory(Base):
    __tablename__ = "productcategory"

    id = Column(Integer, primary_key=True)
    product_name = Column(String, unique=True, index=True)
    image_data = Column(LargeBinary)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc).replace(microsecond=0))

    purchases = relationship("ProductPurchaseTracking", back_populates="product_category")
    orderitem = relationship("OrderItem", back_populates="product_category")
    product = relationship("Product", back_populates="product_category")


class ProductPurchaseTracking(Base):
    __tablename__ = "productpurchasetracking"

    id = Column(Integer, primary_key=True)
    date_purchased = Column(Date, nullable=False, index=True)
    product_name = Column(String, nullable=False)
    product_category_id = Column(Integer, ForeignKey("productcategory.id"))
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc).replace(microsecond=0))
    Quantity = Column(Integer, nullable=False)
    per_cost = Column(Float, nullable=False)
    total_cost = Column(Float, nullable=False)

    product_category = relationship("ProductCategory", back_populates="purchases")


class Product(Base):
    __tablename__ = "product"

    id = Column(Integer, primary_key=True)
    product_name = Column(String, unique=True, index=True)
    price = Column(Float)
    stock = Column(Integer)
    product_category_id = Column(Integer, ForeignKey("productcategory.id"))
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc).replace(microsecond=0))
    updated_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc).replace(microsecond=0),
        onupdate=lambda: datetime.now(timezone.utc).replace(microsecond=0)
    )

    product_category = relationship("ProductCategory", back_populates="product")

    orderitems = relationship("OrderItem", back_populates="product")


class Order(Base):
    __tablename__ = "order"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    total_amount = Column(Float, nullable=False)
    customer_name = Column(String)
    customer_email = Column(String)
    payment_method = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc).replace(microsecond=0))

    user = relationship("User", back_populates="orders")
    orderitems = relationship("OrderItem", back_populates="order")


class OrderItem(Base):
    __tablename__ = "orderitem"

    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey("order.id"))
    product_id = Column(Integer, ForeignKey("product.id"))
    product_category_id = Column(Integer, ForeignKey("productcategory.id"))
    quantity = Column(Integer, nullable=False)
    sales_price = Column(Float)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc).replace(microsecond=0))

    product = relationship("Product", back_populates="orderitems")
    order = relationship("Order", back_populates="orderitems")
    product_category = relationship("ProductCategory", back_populates="orderitem")
