from fastapi import FastAPI
import redis.asyncio as redis
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from contextlib import asynccontextmanager
from src.utils.db import Base, engine
from src.tasks.router import task_routes
from src.user.router import user_routes

Base.metadata.create_all(engine)

@asynccontextmanager
async def lifespan(app: FastAPI):
    redis_url = "redis://redis:6379"
    redis_client = redis.from_url(redis_url)
    FastAPICache.init(RedisBackend(redis_client), prefix="fastapi-cache")
    yield

app = FastAPI(lifespan=lifespan,title="Pybase project")
app.include_router(task_routes)
app.include_router(user_routes)
