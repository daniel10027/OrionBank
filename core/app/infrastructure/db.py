from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base

_engine = None
AsyncSessionLocal: async_sessionmaker[AsyncSession] | None = None
Base = declarative_base()

async def init_engine(dsn: str) -> None:
    global _engine, AsyncSessionLocal
    _engine = create_async_engine(dsn, echo=False, pool_pre_ping=True)
    AsyncSessionLocal = async_sessionmaker(_engine, expire_on_commit=False, class_=AsyncSession)

async def get_session() -> AsyncGenerator[AsyncSession, None]:
    assert AsyncSessionLocal is not None, "DB not initialized"
    async with AsyncSessionLocal() as session:
        yield session