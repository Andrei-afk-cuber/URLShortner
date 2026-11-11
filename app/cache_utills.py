from contextlib import asynccontextmanager

import redis.asyncio as redis
from fastapi import FastAPI

from .config import settings


# Life span for redis right creation
@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.redis = redis.Redis(
        host=settings.redis.host,
        port=settings.redis.port,
        password=settings.redis.password,
        decode_responses=True,
    )
    try:
        yield
    finally:
        await app.state.redis.close()
