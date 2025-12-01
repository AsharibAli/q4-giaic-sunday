from pydantic import BaseModel, EmailStr
import uuid
from datetime import datetime


class UserBase(BaseModel):
    username: str
    email: EmailStr


class UserCreate(UserBase):
    password: str


class User(UserBase):
    user_id: uuid.UUID
    created_at: datetime

    class Config:
        from_attributes = True
