import redis
import asyncio

async def load_monitors_to_redis(cache,key):
    monitors = cache.get(key)
    pass