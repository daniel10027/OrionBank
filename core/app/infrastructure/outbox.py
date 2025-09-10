import asyncio
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession
from .db import AsyncSessionLocal
from .models import OutboxEventORM
from .kafka_producer import KafkaProducer

class OutboxDispatcher:
    def __init__(self, *, bootstrap_servers: str, outbox_topic: str, dlq_topic: str):
        self.bootstrap_servers = bootstrap_servers
        self.outbox_topic = outbox_topic
        self.dlq_topic = dlq_topic
        self._producer: KafkaProducer | None = None
        self._task: asyncio.Task | None = None
        self._stop = asyncio.Event()

    async def start(self):
        self._producer = KafkaProducer(bootstrap_servers=self.bootstrap_servers, client_id="core-outbox")
        await self._producer.start()
        self._task = asyncio.create_task(self._run())

    async def stop(self):
        self._stop.set()
        if self._task:
            await self._task
        if self._producer:
            await self._producer.stop()

    async def _run(self):
        assert AsyncSessionLocal is not None
        while not self._stop.is_set():
            async with AsyncSessionLocal() as session:
                await self._drain_once(session)
            await asyncio.sleep(0.5)

    async def _drain_once(self, session: AsyncSession):
        rows = (await session.execute(select(OutboxEventORM).where(OutboxEventORM.status == "pending").limit(100))).scalars().all()
        if not rows:
            return
        assert self._producer is not None
        for row in rows:
            try:
                await self._producer.send(row.topic, value=row.payload, key=row.key)
                await session.execute(update(OutboxEventORM).where(OutboxEventORM.id == row.id).values(status="sent"))
            except Exception:
                await session.execute(update(OutboxEventORM).where(OutboxEventORM.id == row.id).values(status="failed"))
        await session.commit()