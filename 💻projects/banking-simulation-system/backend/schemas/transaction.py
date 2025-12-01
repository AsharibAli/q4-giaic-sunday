from pydantic import BaseModel
import uuid
from datetime import datetime
from decimal import Decimal


class TransactionBase(BaseModel):
    transaction_type: str
    amount: Decimal


class TransactionCreate(TransactionBase):
    account_id: uuid.UUID
    balance_after_transaction: Decimal


class Transaction(TransactionBase):
    transaction_id: uuid.UUID
    account_id: uuid.UUID
    timestamp: datetime
    balance_after_transaction: Decimal

    class Config:
        from_attributes = True


class DepositWithdraw(BaseModel):
    account_id: uuid.UUID
    amount: Decimal


class Transfer(BaseModel):
    from_account_id: uuid.UUID
    to_account_id: uuid.UUID
    amount: Decimal
