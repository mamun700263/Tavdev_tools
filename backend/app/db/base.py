from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass

# Import all models here so Alembic can detect them
from app.accounts.models import Account, AdminProfile, CompanyProfile, UserProfile  # noqa: E402, F401
from app.uptime_keeper.models import UptimeMonitor, UptimePing