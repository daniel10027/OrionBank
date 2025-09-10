import asyncio
import json
from aiokafka import AIOKafkaProducer
from ..config import settings

class KafkaProducer:
    def __init__(self):
        self._producer = AIOKafkaProducer(
            bootstrap_servers=settings.kafka_bootstrap,
            client_id=settings.kafka_client_id,
            value_serializer=lambda v: json.dumps(v).encode("utf-8"),
            key_serializer=lambda v: v.encode("utf-8") if v else None,
        )
        self._loop = asyncio.new_event_loop()
        self._started = False

    def start(self):
        if self._started:
            return
        def run():
            asyncio.set_event_loop(self._loop)
            self._loop.run_until_complete(self._producer.start())
            self._loop.run_forever()
        import threading
        t = threading.Thread(target=run, daemon=True)
        t.start()
        self._started = True

    def stop(self):
        if not self._started:
            return
        async def shutdown():
            await self._producer.stop()
        self._loop.call_soon_threadsafe(lambda: asyncio.create_task(shutdown()))

    def send(self, topic: str, value: dict, key: str | None = None):
        async def _send():
            await self._producer.send_and_wait(topic, value=value, key=key)
        self._loop.call_soon_threadsafe(lambda: asyncio.create_task(_send()))

producer = KafkaProducer()