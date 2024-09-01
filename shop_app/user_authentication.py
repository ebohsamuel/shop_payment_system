from datetime import datetime, timedelta, timezone
from typing import Annotated
from sqlalchemy.orm import Session
import jwt
from fastapi import Depends, HTTPException, status, Request
from jwt.exceptions import InvalidTokenError, ExpiredSignatureError
from fastapi.templating import Jinja2Templates
from shop_app import models, database
from shop_app.schemas import schemas_user
from shop_app.crud import crud_user


templates = Jinja2Templates(directory="shop_app/templates")

SECRET_KEY = "ec74be764e3ff9ca044d6b13094bbcfad3c70e190410c01c233b0428a5ce67a5"
ALGORITHM = "HS256"

models.Base.metadata.create_all(bind=database.engine)


def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


def authenticate_user(db: Session, email: str, password: str):
    user_data = crud_user.get_user_by_email(db, email)
    if not user_data:
        return False
    if not crud_user.pwd_context.verify(password, user_data.hashed_password):
        return False
    return user_data


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(request: Request, db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    # Extract the token from the 'access_token' cookie
    token = request.cookies.get("access_token")
    if token is None or not token.startswith("Bearer "):
        raise credentials_exception

    # Remove 'Bearer ' prefix
    token = token[len("Bearer "):]

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = schemas_user.TokenData(username=email)
    except ExpiredSignatureError:
        raise credentials_exception
    except InvalidTokenError:
        raise credentials_exception
    user_data = crud_user.get_user_by_email(db, email=token_data.username)
    if user_data is None:
        raise credentials_exception
    return user_data


async def get_current_active_user(current_user: Annotated[schemas_user.User, Depends(get_current_user)]):
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


async def check_admin(user_admin: schemas_user.UserCreate = Depends(get_current_active_user)):
    if not user_admin.is_admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You do not have the necessary permissions.")
    return user_admin
