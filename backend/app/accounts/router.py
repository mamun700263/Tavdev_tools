# app/accounts/router.py

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session

import app.accounts.crud as crud
from app.accounts.auth import (create_access_token, create_refresh_token,
                               decode_token)
from app.accounts.dependencies import get_current_account
from app.accounts.models import Account
from app.accounts.models.account import AccountStatus
from app.accounts.schemas import (AccountCreate, AccountLogin, AccountResponse,
                                  AccountStatusUpdate, TokenRefresh)
from app.db import get_db

router = APIRouter()


# ── AUTH ──────────────────────────────────────────────────


@router.post("/register", response_model=AccountResponse)
def register(data: AccountCreate, db: Session = Depends(get_db)):
    return crud.create_account(db, data)


@router.post("/login")
def login(data: AccountLogin, request: Request, db: Session = Depends(get_db)):
    account = crud.login_account(db, data.email, data.password, request.client.host)
    return {
        "access_token": create_access_token(account.id, account.role),
        "refresh_token": create_refresh_token(account.id),
        "token_type": "bearer",
    }


@router.post("/refresh")
def refresh(data: TokenRefresh, db: Session = Depends(get_db)):
    payload = decode_token(data.refresh_token)

    if payload.get("type") != "refresh":
        raise HTTPException(status_code=401, detail="Invalid token type")

    account_id = payload.get("sub")
    if not account_id:
        raise HTTPException(status_code=401, detail="Invalid token")

    account = db.get(Account, account_id)
    if not account:
        raise HTTPException(status_code=401, detail="Account not found")

    if account.status != AccountStatus.ACTIVE:
        raise HTTPException(status_code=403, detail=f"Account is {account.status}")

    return {
        "access_token": create_access_token(account.id, account.role),
        "token_type": "bearer",
    }


# ── ACCOUNT — ME (must be before /{account_id}) ──────────


@router.get("/me", response_model=AccountResponse)
def get_me(current_account: Account = Depends(get_current_account)):
    return current_account


@router.patch("/me/status", response_model=AccountResponse)
def update_my_status(
    data: AccountStatusUpdate,
    current_account: Account = Depends(get_current_account),
    db: Session = Depends(get_db),
):
    return crud.update_account_status(db, current_account.id, data.status)


# ── ACCOUNT — ADMIN OPERATIONS ────────────────────────────


@router.get("/", response_model=list[AccountResponse])
def list_accounts(db: Session = Depends(get_db)):
    return crud.get_all_accounts(db)


@router.get("/{account_id}", response_model=AccountResponse)
def get_account(account_id: UUID, db: Session = Depends(get_db)):
    return crud.get_account_by_id(db, account_id)


@router.patch("/{account_id}/status", response_model=AccountResponse)
def update_status(
    account_id: UUID,
    data: AccountStatusUpdate,
    db: Session = Depends(get_db),
):
    return crud.update_account_status(db, account_id, data.status)


@router.delete("/{account_id}")
def delete_account(account_id: UUID, db: Session = Depends(get_db)):
    return crud.delete_account(db, account_id)
