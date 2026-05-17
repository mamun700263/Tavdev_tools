import asyncio
from datetime import datetime, timezone

from app.db.engine import SessionLocal
from app.uptime_keeper.models import UptimeMonitor, UptimePing
from app.uptime_keeper.ping import ping

# tracks the last time each monitor was pinged
# { monitor_id: datetime }
_last_pinged: dict = {}


async def run_monitor(monitor: UptimeMonitor, db):
    print(f"[uptime] pinging {monitor.name} → {monitor.url}", flush=True)
    result = await ping(monitor.url)

    ping_record = UptimePing(
        monitor_id=monitor.id,
        **result
    )
    db.add(ping_record)
    db.commit()
    print(f"[uptime] saved ping for {monitor.name} → up={result['is_up']}", flush=True)


async def scheduler():
    print("[uptime] scheduler started", flush=True)

    while True:
        db = SessionLocal()
        try:
            now = datetime.now(timezone.utc)

            # pull all active monitors from DB
            monitors = db.query(UptimeMonitor).filter(
                UptimeMonitor.is_active == True
            ).all()

            due = []
            for monitor in monitors:
                last = _last_pinged.get(monitor.id)
                interval_seconds = monitor.interval_minutes * 60

                # ping if never pinged before, or interval has passed
                if last is None or (now - last).total_seconds() >= interval_seconds:
                    due.append(monitor)
                    _last_pinged[monitor.id] = now

            if due:
                print(f"[uptime] {len(due)} monitors due for ping", flush=True)
                await asyncio.gather(*[run_monitor(m, db) for m in due])
            else:
                print("[uptime] no monitors due", flush=True)

        except Exception as e:
            print(f"[uptime] scheduler error: {e}", flush=True)
        finally:
            db.close()

        # check every 30 seconds
        await asyncio.sleep(30)