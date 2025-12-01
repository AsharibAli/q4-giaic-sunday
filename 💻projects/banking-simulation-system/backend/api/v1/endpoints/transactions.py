from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import uuid
from decimal import Decimal

from ....crud import account as crud_account
from ....crud import transaction as crud_transaction
from ....schemas import account as account_schema
from ....schemas import transaction as transaction_schema
from ....schemas import user as user_schema
from ....db.database import get_db
from ..dependencies import get_current_user

router = APIRouter()


@router.post("/deposit", response_model=account_schema.Account)
def deposit(
    deposit: transaction_schema.DepositWithdraw,
    db: Session = Depends(get_db),
    current_user: user_schema.User = Depends(get_current_user),
):
    account = crud_account.get_account(db, account_id=deposit.account_id)
    if not account or account.user_id != current_user.user_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Account not found"
        )
    updated_account = crud_transaction.deposit(
        db, account_id=deposit.account_id, amount=deposit.amount
    )
    return updated_account


@router.post("/withdraw", response_model=account_schema.Account)
def withdraw(
    withdraw: transaction_schema.DepositWithdraw,
    db: Session = Depends(get_db),
    current_user: user_schema.User = Depends(get_current_user),
):
    account = crud_account.get_account(db, account_id=withdraw.account_id)
    if not account or account.user_id != current_user.user_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Account not found"
        )
    if account.balance < withdraw.amount:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Insufficient funds"
        )
    updated_account = crud_transaction.withdraw(
        db, account_id=withdraw.account_id, amount=withdraw.amount
    )
    return updated_account


@router.post("/transfer")
def transfer(
    transfer: transaction_schema.Transfer,
    db: Session = Depends(get_db),
    current_user: user_schema.User = Depends(get_current_user),
):
    from_account = crud_account.get_account(db, account_id=transfer.from_account_id)
    to_account = crud_account.get_account(db, account_id=transfer.to_account_id)

    if not from_account or from_account.user_id != current_user.user_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Source account not found"
        )
    if not to_account:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Destination account not found"
        )
    # Check if the user owns the 'to_account'
    if to_account.user_id != current_user.user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Cannot transfer to another user's account"
        )

    if from_account.balance < transfer.amount:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Insufficient funds"
        )

    crud_transaction.transfer(
        db,
        from_account_id=transfer.from_account_id,
        to_account_id=transfer.to_account_id,
        amount=transfer.amount,
    )
    return {"message": "Transfer successful"}


@router.get("/{account_id}", response_model=list[transaction_schema.Transaction])
def read_transactions(
    account_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: user_schema.User = Depends(get_current_user),
):
    account = crud_account.get_account(db, account_id=account_id)
    if not account or account.user_id != current_user.user_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Account not found"
        )
    transactions = crud_transaction.get_transactions_by_account(db, account_id=account_id)
    return transactions
