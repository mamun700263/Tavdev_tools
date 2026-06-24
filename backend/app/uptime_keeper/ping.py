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
            st = {
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
            try:
                from app.core.data_exporters import GoogleSheetPusher
                sheet= GoogleSheetPusher('Tavdev Monitor')
                st["base_url"] = url
                st["checked_at"] = checked_at.isoformat()
                sheet.append_row(st, "passed")
            except Exception as e:
                print("GOOGLE SHEET ERROR:", repr(e))
                raise
            return st

    except httpx.TimeoutException:
        error_type = "timeout"
    except httpx.ConnectError:
        error_type = "connection_refused"
    except Exception:
        error_type = "http_error"
    
    return {
        "is_up": False,
        "status_code": None,
        "response_time_ms": None,
        "error_type": None,
        "checked_at": checked_at,
    }

