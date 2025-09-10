import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI
from core.app.infrastructure.db import init_engine
from core.app.infrastructure.outbox import OutboxDispatcher
from core.app.config import settings

dispatcher: OutboxDispatcher | None = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    # DB engine
    await init_engine(settings.db_dsn)
    # Outbox dispatcher
    global dispatcher
    dispatcher = OutboxDispatcher(
        bootstrap_servers=settings.kafka_bootstrap,
        outbox_topic=settings.kafka_outbox_topic,
        dlq_topic=settings.kafka_dlq_topic,
    )
    await dispatcher.start()
    try:
        yield
    finally:
        if dispatcher:
            await dispatcher.stop()