from contextlib import asynccontextmanager
from fastapi import FastAPI
import asyncio

from .uptime_keeper.scheduler import scheduler
from app.uptime_keeper.caching.db_to_redis import sync_all_monitors


@asynccontextmanager
async def lifespan(app: FastAPI):

    # -------------------
    # STARTUP
    # -------------------
    sync_all_monitors()
    task = asyncio.create_task(scheduler())
    app.state.scheduler_task = task

    try:
        yield

    finally:
        # -------------------
        # SHUTDOWN
        # -------------------
        task.cancel()

        try:
            await task
        except asyncio.CancelledError:
            print("[uptime] scheduler stopped")