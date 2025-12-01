import uuid
from sqlalchemy import (
    Column,
    DateTime,
    ForeignKey,
    Numeric,
    String,
    func,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    user_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime, default=func.now())
    accounts = relationship("Account", back_populates="user")


class Account(Base):
    __tablename__ = "accounts"
    account_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.user_id"), nullable=False)
    account_type = Column(String, nullable=False)
    balance = Column(Numeric(15, 2), nullable=False, default=0.00)
    created_at = Column(DateTime, default=func.now())
    user = relationship("User", back_populates="accounts")
    transactions = relationship("Transaction", back_populates="account")


class Transaction(Base):
    __tablename__ = "transactions"
    transaction_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    account_id = Column(
        UUID(as_uuid=True), ForeignKey("accounts.account_id"), nullable=False
    )
    transaction_type = Column(String, nullable=False)
    amount = Column(Numeric(15, 2), nullable=False)
    timestamp = Column(DateTime, default=func.now())
    balance_after_transaction = Column(Numeric(15, 2), nullable=False)
    account = relationship("Account", back_populates="transactions")
