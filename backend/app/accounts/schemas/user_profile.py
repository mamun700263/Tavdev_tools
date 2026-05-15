from uuid import UUID

import pytz
from pydantic import BaseModel, HttpUrl, field_validator

# ── INPUT SCHEMAS ─────────────────────────────────────────


class UserProfileCreate(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    phone: str | None = None
    avatar_url: str | None = None
    timezone: str | None = None
    notification_preferences: dict | None = None

    @field_validator("timezone")
    @classmethod
    def validate_timezone(cls, v):
        if v is not None and v not in pytz.all_timezones:
            raise ValueError(f"Invalid timezone: {v}")
        return v

    @field_validator("notification_preferences")
    @classmethod
    def validate_notification_prefs(cls, v):
        if v is not None:
            allowed_keys = {"email", "sms"}
            invalid = set(v.keys()) - allowed_keys
            if invalid:
                raise ValueError(f"Invalid notification keys: {invalid}")
            if not all(isinstance(val, bool) for val in v.values()):
                raise ValueError("Notification values must be booleans")
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


class UserProfileUpdate(UserProfileCreate):
    pass  # same fields, all optional — PATCH behavior


# ── OUTPUT SCHEMAS ────────────────────────────────────────


class UserProfileResponse(BaseModel):
    id: UUID
    account_id: UUID
    first_name: str | None
    last_name: str | None
    phone: str | None
    avatar_url: str | None
    timezone: str | None
    notification_preferences: dict | None
    display_name: str | None  # computed from the model method

    class Config:
        from_attributes = True
