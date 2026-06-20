import httpx
from datetime import datetime, timezone


async def normalize_url(url: str) -> str:
    url = url.strip()
    if not url.startswith(("http://", "https://")):
        url = f"https://{url}"
    return url


async def ping(url: str) -> dict:
    checked_at = datetime.now(timezone.utc)
    url = await normalize_url(url)

    try:
        async with httpx.AsyncClient(follow_redirects=True, timeout=10) as client:
            start = datetime.now(timezone.utc)

            r = await client.get(url)

            elapsed_ms = int(
                (datetime.now(timezone.utc) - start).total_seconds() * 1000
            )

            redirect_count = len(r.history)

            return {
                # LAYER A: availability
                "is_up": True,
                "status_code": r.status_code,
                "reason": r.reason_phrase,

                # LAYER B: performance
                "response_time_ms": elapsed_ms,

                # LAYER C: routing
                "final_url": str(r.url),
                "redirect_count": redirect_count,
                "http_version": r.http_version,

                # LAYER D: metadata
                "content_type": r.headers.get("content-type"),
                "content_length": len(r.content) if r.content else 0,

                # meta
                "checked_at": checked_at,
                "error_message": None,
            }

    except Exception as e:
        return {
            "is_up": False,
            "status_code": None,
            "response_time_ms": None,
            "error_type": "timeout" | "dns_failure" | "connection_refused" | "ssl_error" | "http_error" | None,
            "checked_at": checked_at,
        }
    
