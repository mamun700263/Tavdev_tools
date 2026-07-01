import json,os
from app.core.redis import redis_client
from app.db.engine import SessionLocal
from app.uptime_keeper.models import UptimeMonitor
from datetime import datetime, timezone

SCHEDULE_KEY =os.getenv('SCHEDULE_KEY')
UPTIME_MONITOR=os.getenv('UPTIME_MONITOR')

def sync_monitor_to_redis(monitor: UptimeMonitor):
    key = f"{UPTIME_MONITOR}{monitor.id}"

    data = {
        "id": str(monitor.id),
        "url": monitor.url,
        "interval": monitor.interval_minutes,
        "is_active": monitor.is_active,
        "last_pinged": None
    }

    redis_client.set(key, json.dumps(data))

    now = datetime.now(timezone.utc).timestamp()

    redis_client.zadd(
        SCHEDULE_KEY,
        {
            str(monitor.id): now
        }
    )



def sync_all_monitors():
    db = SessionLocal()
    try:
        monitors = db.query(UptimeMonitor).all()

        for m in monitors:
            sync_monitor_to_redis(m)

        print(f"[redis-sync] synced {len(monitors)} monitors")

    finally:
        db.close()