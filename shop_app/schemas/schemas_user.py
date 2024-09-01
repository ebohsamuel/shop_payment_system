from pydantic import BaseModel
from datetime import datetime


class UserBase(BaseModel):
    email: str
    fullname: str
    is_admin: bool


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class ConfigDict:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None
