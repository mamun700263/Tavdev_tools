import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI

from .scheduler import scheduler


@asynccontextmanager
async def lifespan(app: FastAPI):
    asyncio.create_task(scheduler())
    yield
