from collections.abc import AsyncGenerator

import redis.asyncio as redis
from app.main import app
from fastapi import FastAPI

from configs.settings import settings


# Инициализирует Redis и кладёт клиент в app.state
async def init_redis(app: FastAPI) -> None:
    app.state.redis = redis.from_url(
        settings.REDIS_URL,
        decode_responses=True,
    )
    await app.state.redis.ping()


# Dependency, достаёт уже созданный клиент из app.state
async def get_redis() -> AsyncGenerator[redis.Redis, None]:
    if not hasattr(app.state, "redis"):
        app.state.redis = redis.from_url(
            settings.REDIS_URL,
            decode_responses=True,
        )
        await app.state.redis.ping()
    yield app.state.redis
