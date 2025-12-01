from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from ....crud import user, account
from ....schemas import user as user_schema
from ....schemas import account as account_schema
from ....core import security
from ....db.database import get_db

router = APIRouter()


@router.post("/register", response_model=schemas.user.User)
def register(user: schemas.user.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.user.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )
    db_user = crud.user.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered",
        )
    new_user = crud.user.create_user(db=db, user=user)

    # Create checking and savings accounts
    crud.account.create_user_account(
        db=db,
        account=schemas.account.AccountCreate(account_type="checking"),
        user_id=new_user.user_id,
    )
    crud.account.create_user_account(
        db=db,
        account=schemas.account.AccountCreate(account_type="savings"),
        user_id=new_user.user_id,
    )

    return new_user


@router.post("/login")
def login(
    db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()
):
    user = crud.user.get_user_by_username(db, username=form_data.username)
    if not user or not security.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = security.create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}
