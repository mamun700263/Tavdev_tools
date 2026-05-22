from fastapi import APIRouter, Query
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db import get_db
from app.uptime_keeper import crud, schemas

from .ping import ping

router = APIRouter()


@router.get(
    "/test-ping",
    summary="check health of  a URL",
    description="Checks whether a given URL is reachable and returns the response time. Useful for uptime monitoring or pre-scrape health checks.",
)
async def test_ping(
    url: str = Query(
        ...,
        description="The full URL to ping, including scheme.",
        example="https://example.com",
    )
):
    """
    Ping a URL to check its reachability.

    - **url**: Must include `http://` or `https://`
    - Returns response time in milliseconds if reachable
    - Returns `reachable: false` if the host is down or times out
    """
    result = await ping(url)
    return result




# ------------------------
# MONITORS
# ------------------------

@router.post("/monitors", response_model=schemas.UptimeMonitorOut)
def create_monitor(payload: schemas.UptimeMonitorCreate, db: Session = Depends(get_db)):
    return crud.create_monitor(db, payload)


@router.get("/monitors/{monitor_id}", response_model=schemas.UptimeMonitorOut)
def get_monitor(monitor_id, db: Session = Depends(get_db)):
    obj = crud.get_monitor(db, monitor_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Monitor not found")
    return obj

@router.get("/motinor_count/", response_model=int)
def get_monitor_count(db:Session=Depends(get_db)):
    return crud.count_monitors(db)

@router.get("/accounts/{account_id}/monitors", response_model=list[schemas.UptimeMonitorOut])
def list_monitors(account_id, db: Session = Depends(get_db)):
    return crud.get_monitors_by_account(db, account_id)


@router.patch("/monitors/{monitor_id}", response_model=schemas.UptimeMonitorOut)
def update_monitor(monitor_id, payload: schemas.UptimeMonitorUpdate, db: Session = Depends(get_db)):
    obj = crud.update_monitor(db, monitor_id, payload)
    if not obj:
        raise HTTPException(status_code=404, detail="Monitor not found")
    return obj


@router.delete("/monitors/{monitor_id}")
def delete_monitor(monitor_id, db: Session = Depends(get_db)):
    obj = crud.delete_monitor(db, monitor_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Monitor not found")
    return {"deleted": True}


# ------------------------
# PINGS
# ------------------------

@router.get("/monitors/{monitor_id}/pings", response_model=list[schemas.UptimePingOut])
def list_pings(monitor_id, db: Session = Depends(get_db)):
    return crud.get_pings_by_monitor(db, monitor_id)