# app/accounts/schemas/admin_profile.py

from uuid import UUID

from pydantic import BaseModel, field_validator

# ── INPUT SCHEMAS ─────────────────────────────────────────


class AdminProfileCreate(BaseModel):
    is_super_admin: bool = False
    permissions: dict | None = None

    @field_validator("permissions")
    @classmethod
    def validate_permissions(cls, v):
        if v is not None:
            # all keys must be "resource.action" format
            # all values must be booleans
            for key, val in v.items():
                if not isinstance(val, bool):
                    raise ValueError(f"Permission value for '{key}' must be a boolean")
                if "." not in key:
                    raise ValueError(
                        f"Permission key '{key}' must be in 'resource.action' format"
                        " e.g. 'users.manage'"
                    )
        return v


class AdminProfileUpdate(AdminProfileCreate):
    is_super_admin: bool | None = None  # optional for PATCH


# ── OUTPUT SCHEMAS ────────────────────────────────────────


class AdminProfileResponse(BaseModel):
    id: UUID
    account_id: UUID
    is_super_admin: bool
    permissions: dict | None

    class Config:
        from_attributes = True
