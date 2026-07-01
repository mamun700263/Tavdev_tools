import asyncio,os
from datetime import datetime, timezone

from app.core.redis import redis_client
from app.db.engine import SessionLocal
from app.uptime_keeper.models import UptimeMonitor, UptimePing
from app.uptime_keeper.ping import ping,to_uptime_ping


SCHEDULE_KEY =os.getenv('SCHEDULE_KEY')


# -------------------------
# SINGLE MONITOR EXECUTION
# -------------------------
async def handle_monitor(monitor_id: str):
    db = SessionLocal()
    try:
        monitor = (
            db.query(UptimeMonitor)
            .filter(UptimeMonitor.id == monitor_id)
            .first()
        )

        if not monitor or not monitor.is_active:
            return

        print(f"[uptime] pinging {monitor.name} → {monitor.url}", flush=True)

        result = await ping(monitor.url)
        result = to_uptime_ping(result)
        db.add(
            UptimePing(
                monitor_id=monitor.id,
                **result
            )
        )
        db.commit()

        # -------------------------
        # RESCHEDULE (ONLY AFTER SUCCESSFUL EXECUTION)
        # -------------------------
        next_run = datetime.now(timezone.utc).timestamp() + (
            monitor.interval_minutes * 60
        )

        redis_client.zadd(
            SCHEDULE_KEY,
            {str(monitor.id): next_run}
        )

    except Exception as e:
        print(f"[uptime] monitor failed {monitor_id}: {repr(e)}")

    finally:
        db.close()


# -------------------------
# SCHEDULER LOOP
# -------------------------
async def scheduler():
    print("[uptime] redis scheduler started", flush=True)

    while True:
        try:
            now_ts = datetime.now(timezone.utc).timestamp()
            

            # -----------------------------------
            # ATOMIC CLAIM (prevents duplicates)
            # -----------------------------------
            due = redis_client.zrangebyscore(
                SCHEDULE_KEY,
                0,
                now_ts
            )

            if not due:
                print("[uptime] no monitors due")
                await asyncio.sleep(30)
                continue

            # IMPORTANT: convert bytes → str
            monitor_ids = [m for m in due]
            print(monitor_ids)

            # remove from schedule BEFORE execution (claiming step)
            redis_client.zrem(SCHEDULE_KEY, *due)

            print(f"[uptime] due monitors: {len(monitor_ids)}")

            # run concurrently (safe now because DB sessions are isolated)
            tasks = [
                handle_monitor(monitor_id)
                for monitor_id in monitor_ids
            ]

            await asyncio.gather(*tasks)

        except Exception as e:
            print("[uptime] scheduler error:", repr(e))

        await asyncio.sleep(30)