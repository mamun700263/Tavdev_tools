import redis
import os

redis_client = redis.from_url(
    os.getenv("CACHE_URL"),
    decode_responses=True
)