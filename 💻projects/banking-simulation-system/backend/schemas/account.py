from pydantic import BaseModel
import uuid
from datetime import datetime
from decimal import Decimal


class AccountBase(BaseModel):
    account_type: str


class AccountCreate(AccountBase):
    balance: Decimal = 0.00


class Account(AccountBase):
    account_id: uuid.UUID
    user_id: uuid.UUID
    balance: Decimal
    created_at: datetime

    class Config:
        from_attributes = True
