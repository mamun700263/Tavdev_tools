# app/accounts/schemas/company_profile.py

import re
from uuid import UUID

from pydantic import BaseModel, field_validator

# ── INPUT SCHEMAS ─────────────────────────────────────────


class CompanyProfileCreate(BaseModel):
    company_name: str
    company_logo_url: str | None = None
    address: str | None = None
    phone: str | None = None
    domain: str | None = None
    billing_plan: str | None = None
    settings: dict | None = None

    @field_validator("company_name")
    @classmethod
    def validate_company_name(cls, v):
        if len(v.strip()) < 2:
            raise ValueError("Company name must be at least 2 characters")
        return v.strip()

    @field_validator("domain")
    @classmethod
    def validate_domain(cls, v):
        if v is not None:
            pattern = (
                r"^(?:[a-zA-Z0-9](?:[a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,}$"
            )
            if not re.match(pattern, v):
                raise ValueError("Invalid domain format. Example: company.com")
        return v

    @field_validator("phone")
    @classmethod
    def validate_phone(cls, v):
        if v is not None:
            cleaned = v.replace("+", "").replace(" ", "").replace("-", "")
            if not cleaned.isdigit():
                raise ValueError("Phone must contain only digits, +, spaces, or dashes")
            if not (7 <= len(cleaned) <= 15):
                raise ValueError("Phone must be between 7 and 15 digits")
        return v


class CompanyProfileUpdate(CompanyProfileCreate):
    company_name: str | None = None  # override — make optional for PATCH


# ── OUTPUT SCHEMAS ────────────────────────────────────────


class CompanyProfileResponse(BaseModel):
    id: UUID
    account_id: UUID
    company_name: str
    company_logo_url: str | None
    address: str | None
    phone: str | None
    domain: str | None
    billing_plan: str | None
    settings: dict | None

    class Config:
        from_attributes = True
