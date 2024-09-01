from sqlalchemy.orm import Session
from passlib.context import CryptContext
from shop_app.schemas import schemas_user
from shop_app import models


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_user(db: Session, user_data: schemas_user.UserCreate):
    hashed_password = pwd_context.hash(user_data.password)
    db_user = models.User(
        email=user_data.email, hashed_password=hashed_password,
        fullname=user_data.fullname, is_admin=user_data.is_admin
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_user_by_id(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_users(db: Session):
    return db.query(models.User).all()


def update_user(db: Session, user_details: dict, user_id: int):
    db_user = get_user_by_id(db, user_id)
    db_user.is_active = user_details["is_active"]
    if user_details["fullname"]:
        db_user.fullname = user_details["fullname"]
    if user_details["email"]:
        db_user.email = user_details["email"]
    if user_details["password"]:
        db_user.password = pwd_context.hash(user_details["password"])
    db.commit()
    db.refresh(db_user)
    return db_user
