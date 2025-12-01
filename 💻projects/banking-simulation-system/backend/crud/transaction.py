from sqlalchemy.orm import Session
from ..db import models
from ..schemas import transaction as transaction_schema
import uuid
from decimal import Decimal


def create_transaction(
    db: Session, transaction: transaction_schema.TransactionCreate
):
    db_transaction = models.Transaction(**transaction.model_dump())
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    return db_transaction


def get_transactions_by_account(
    db: Session, account_id: uuid.UUID, skip: int = 0, limit: int = 100
):
    return (
        db.query(models.Transaction)
        .filter(models.Transaction.account_id == account_id)
        .order_by(models.Transaction.timestamp.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )


def deposit(db: Session, account_id: uuid.UUID, amount: Decimal):
    account = db.query(models.Account).filter(models.Account.account_id == account_id).first()
    if not account:
        return None
    account.balance += amount
    transaction = models.Transaction(
        account_id=account_id,
        transaction_type="deposit",
        amount=amount,
        balance_after_transaction=account.balance,
    )
    db.add(transaction)
    db.commit()
    db.refresh(account)
    return account


def withdraw(db: Session, account_id: uuid.UUID, amount: Decimal):
    account = db.query(models.Account).filter(models.Account.account_id == account_id).first()
    if not account or account.balance < amount:
        return None
    account.balance -= amount
    transaction = models.Transaction(
        account_id=account_id,
        transaction_type="withdrawal",
        amount=amount,
        balance_after_transaction=account.balance,
    )
    db.add(transaction)
    db.commit()
    db.refresh(account)
    return account


def transfer(db: Session, from_account_id: uuid.UUID, to_account_id: uuid.UUID, amount: Decimal):
    from_account = (
        db.query(models.Account).filter(models.Account.account_id == from_account_id).first()
    )
    to_account = (
        db.query(models.Account).filter(models.Account.account_id == to_account_id).first()
    )

    if not from_account or not to_account or from_account.balance < amount:
        return None

    from_account.balance -= amount
    to_account.balance += amount

    from_transaction = models.Transaction(
        account_id=from_account_id,
        transaction_type="transfer_out",
        amount=amount,
        balance_after_transaction=from_account.balance,
    )
    to_transaction = models.Transaction(
        account_id=to_account_id,
        transaction_type="transfer_in",
        amount=amount,
        balance_after_transaction=to_account.balance,
    )

    db.add(from_transaction)
    db.add(to_transaction)
    db.commit()

    return from_account, to_account
