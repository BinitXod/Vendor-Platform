# app/main.py
from fastapi import FastAPI
from contextlib import asynccontextmanager
from arq import create_pool
from arq.connections import RedisSettings

from app.config.settings import settings
from app.utils.logger import logger
from app.database.connection import engine
from app.api.v1.router import api_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info(f"Starting up {settings.PROJECT_NAME} in {settings.ENVIRONMENT} mode.")

    # Initialize ARQ Redis Pool and attach to app state
    try:
        app.state.redis = await create_pool(RedisSettings.from_dsn(settings.REDIS_URL))
        logger.info("Connected to Redis for Background Tasks.")
    except Exception as e:
        logger.warning(f"Failed to connect to Redis: {e} (Background tasks will fail)")

    yield

    logger.info("Shutting down application. Disposing database engine.")
    await engine.dispose()
    if hasattr(app.state, 'redis'):
        await app.state.redis.close()


app = FastAPI(title=settings.PROJECT_NAME, version="1.0.0", lifespan=lifespan)
app.include_router(api_router, prefix="/api/v1")