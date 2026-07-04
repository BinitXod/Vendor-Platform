# app/database/connection.py
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from app.config.settings import settings
from app.utils.logger import logger

# Create the async engine
engine = create_async_engine(
    settings.async_database_url,
    echo=(settings.ENVIRONMENT == "development"), # Log SQL queries in dev
    future=True,
    pool_pre_ping=True,
    connect_args={"ssl": True}
)

# Async session factory
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False
)

async def get_db_session():
    """Dependency to provide a database session to FastAPI endpoints."""
    async with AsyncSessionLocal() as session:
        try:
            yield session
        except Exception as e:
            logger.error(f"Database session error: {str(e)}")
            await session.rollback()
            raise
        finally:
            await session.close()