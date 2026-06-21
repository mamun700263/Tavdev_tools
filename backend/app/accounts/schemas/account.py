import string
from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, EmailStr, field_validator

from app.accounts.models.account import AccountStatus, RoleEnum
from app.accounts.schemas.admin import AdminProfileResponse
from app.accounts.schemas.company_profile import CompanyProfileResponse

# import profile schemas — these must be imported AFTER their files exist
from app.accounts.schemas.user_profile import UserProfileResponse


class TokenRefresh(BaseModel):
    refresh_token: str


# ── INPUT SCHEMAS ─────────────────────────────────────────


class AccountCreate(BaseModel):
    email: EmailStr
    password: str
    role: RoleEnum = RoleEnum.USER

    @field_validator("password")
    @classmethod
    def password_strength(cls, v):
        if len(v) < 9:
            raise ValueError("Password must be at least 9 characters")
        if not any(c.isupper() for c in v):
            raise ValueError("Password must contain at least one uppercase letter")
        if not any(c.islower() for c in v):
            raise ValueError("Password must contain at least one lowercase letter")
        if not any(c.isdigit() for c in v):
            raise ValueError("Password must contain at least one number")
        if not any(c in string.punctuation for c in v):
            raise ValueError(
                "Password must contain at least one special character"
            )
        return v


class AccountLogin(BaseModel):
    email: EmailStr
    password: str


class PasswordResetRequest(BaseModel):
    email: EmailStr


class PasswordResetConfirm(BaseModel):
    token: str
    new_password: str


class AccountStatusUpdate(BaseModel):
    status: AccountStatus


# ── OUTPUT SCHEMAS ────────────────────────────────────────


class AccountResponse(BaseModel):
    id: UUID
    email: EmailStr
    role: RoleEnum
    is_verified: bool
    status: AccountStatus
    created_at: datetime
    last_login_at: datetime | None

    class Config:
        from_attributes = True


# AccountMeResponse at the bottom because it depends on
# AccountResponse + all three profile schemas above
class AccountMeResponse(AccountResponse):
    updated_at: datetime
    last_login_ip: str | None
    signup_ip: str | None

    user_profile: UserProfileResponse | None = None
    company_profile: CompanyProfileResponse | None = None
    admin_profile: AdminProfileResponse | None = None
