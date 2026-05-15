# app/accounts/dependencies.py

from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.accounts.auth import decode_token
from app.accounts.models import Account, AccountStatus, RoleEnum
from app.db import get_db

bearer_scheme = HTTPBearer()  # ← shows "Authorize" button with token input in Swagger


def get_current_account(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    db: Session = Depends(get_db),
) -> Account:
    token = credentials.credentials  # ← extracts the actual token string

    payload = decode_token(token)

    if payload.get("type") != "access":
        raise HTTPException(status_code=401, detail="Invalid token type")

    account_id = payload.get("sub")
    if not account_id:
        raise HTTPException(status_code=401, detail="Invalid token")

    account = db.get(Account, account_id)
    if not account:
        raise HTTPException(status_code=401, detail="Account not found")

    if account.status != AccountStatus.ACTIVE:
        raise HTTPException(status_code=403, detail=f"Account is {account.status}")

    return account


def get_current_admin(account: Account = Depends(get_current_account)) -> Account:
    if account.role != RoleEnum.ADMIN:
        raise HTTPException(status_code=403, detail="Admins only")
    return account
