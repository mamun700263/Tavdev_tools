from sqlalchemy.orm import Session
from app.uptime_keeper import models, schemas


# ------------------------
# Uptime Monitor CRUD
# ------------------------

def create_monitor(db: Session, data: schemas.UptimeMonitorCreate):
    payload = data.model_dump()
    payload["url"] = str(payload["url"])
    obj = models.UptimeMonitor(**payload)
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def get_monitor(db: Session, monitor_id):
    return db.query(models.UptimeMonitor).filter(
        models.UptimeMonitor.id == monitor_id
    ).first()


def get_monitors_by_account(db: Session, account_id):
    return db.query(models.UptimeMonitor).filter(
        models.UptimeMonitor.account_id == account_id
    ).all()


def update_monitor(db: Session, monitor_id, data: schemas.UptimeMonitorUpdate):
    obj = get_monitor(db, monitor_id)
    if not obj:
        return None

    for k, v in data.model_dump(exclude_unset=True).items():
        setattr(obj, k, v)

    db.commit()
    db.refresh(obj)
    return obj


def delete_monitor(db: Session, monitor_id):
    obj = get_monitor(db, monitor_id)
    if not obj:
        return None

    db.delete(obj)
    db.commit()
    return obj


# ------------------------
# Uptime Ping CRUD
# ------------------------

def create_ping(db: Session, data: schemas.UptimePingCreate):
    obj = models.UptimePing(**data.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def get_pings_by_monitor(db: Session, monitor_id):
    return db.query(models.UptimePing).filter(
        models.UptimePing.monitor_id == monitor_id
    ).order_by(models.UptimePing.checked_at.desc()).all()