from sqlalchemy.orm import Session
from ..db import models
from ..schemas import account as account_schema
import uuid


def get_account(db: Session, account_id: uuid.UUID):
    return db.query(models.Account).filter(models.Account.account_id == account_id).first()


def get_accounts_by_user(db: Session, user_id: uuid.UUID, skip: int = 0, limit: int = 100):
    return (
        db.query(models.Account)
        .filter(models.Account.user_id == user_id)
        .offset(skip)
        .limit(limit)
        .all()
    )


def create_user_account(
    db: Session, account: account_schema.AccountCreate, user_id: uuid.UUID
):
    db_account = models.Account(**account.model_dump(), user_id=user_id)
    db.add(db_account)
    db.commit()
    db.refresh(db_account)
    return db_account
