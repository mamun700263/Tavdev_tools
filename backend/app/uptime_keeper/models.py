# app/uptime_keeper/models.py

import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Boolean, Integer, DateTime, ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import relationship
from app.db.base import Base


class UptimeMonitor(Base):
    __tablename__ = "uptime_monitors"

    id         = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    account_id = Column(
                    PG_UUID(as_uuid=True),
                    ForeignKey("accounts.id", ondelete="CASCADE"),
                    nullable=False,
                    index=True
                )

    name               = Column(String(100), nullable=False)        # "My API", "Production Server"
    url                = Column(String(2048), nullable=False)        # the URL to ping
    interval_minutes   = Column(Integer, default=5, nullable=False)  # how often to ping
    is_active          = Column(Boolean, default=True, nullable=False)
    created_at         = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at         = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    # relationships
    account = relationship("Account")  # optional
    pings = relationship(
        "UptimePing",
        back_populates="monitor",
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<UptimeMonitor {self.name} ({self.url})>"


class UptimePing(Base):
    __tablename__ = "uptime_pings"

    id         = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    monitor_id = Column(PG_UUID(as_uuid=True), ForeignKey("uptime_monitors.id", ondelete="CASCADE"), nullable=False, index=True)

    is_up            = Column(Boolean, nullable=False)               # True = up, False = down
    status_code      = Column(Integer, nullable=True)                # 200, 404, 500 etc. None if unreachable
    response_time_ms = Column(Integer, nullable=True)                # how long it took in ms
    error_message    = Column(Text, nullable=True)                   # if it failed, why
    checked_at       = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)

    # relationship
    monitor = relationship("UptimeMonitor", back_populates="pings")

    def __repr__(self):
        status = "UP" if self.is_up else "DOWN"
        return f"<UptimePing {status} {self.response_time_ms}ms>"