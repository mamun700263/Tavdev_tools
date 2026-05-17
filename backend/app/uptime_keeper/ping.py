import httpx
from datetime import datetime, timezone


async def ping(url: str) -> dict:
    checked_at = datetime.now(timezone.utc)
    try:
        async with httpx.AsyncClient() as client:
            start = datetime.now(timezone.utc)
            r = await client.get(url, timeout=10)
            elapsed_ms = int((datetime.now(timezone.utc) - start).total_seconds() * 1000)

        return {
            "is_up": True,
            "status_code": r.status_code,
            "response_time_ms": elapsed_ms,
            "error_message": None,
            "checked_at": checked_at,
        }
    except Exception as e:
        return {
            "is_up": False,
            "status_code": None,
            "response_time_ms": None,
            "error_message": str(e),
            "checked_at": checked_at,
        }