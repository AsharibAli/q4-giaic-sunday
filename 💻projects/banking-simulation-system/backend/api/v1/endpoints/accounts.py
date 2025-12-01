from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import uuid

from ....crud import account as crud_account
from ....schemas import account as account_schema
from ....schemas import user as user_schema
from ....db.database import get_db
from ..dependencies import get_current_user

router = APIRouter()


@router.get("/", response_model=list[schemas.account.Account])
def read_accounts(
    db: Session = Depends(get_db),
    current_user: schemas.user.User = Depends(get_current_user),
):
    accounts = crud.account.get_accounts_by_user(db, user_id=current_user.user_id)
    return accounts


@router.get("/{account_id}", response_model=schemas.account.Account)
def read_account(
    account_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: schemas.user.User = Depends(get_current_user),
):
    account = crud.account.get_account(db, account_id=account_id)
    if not account or account.user_id != current_user.user_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Account not found"
        )
    return account
