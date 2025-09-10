import json
from aiokafka import AIOKafkaProducer

class KafkaProducer:
    def __init__(self, *, bootstrap_servers: str, client_id: str):
        self._producer = AIOKafkaProducer(
            bootstrap_servers=bootstrap_servers,
            client_id=client_id,
            value_serializer=lambda v: json.dumps(v).encode("utf-8"),
            key_serializer=lambda v: v.encode("utf-8") if v else None,
        )

    async def start(self):
        await self._producer.start()

    async def stop(self):
        await self._producer.stop()

    async def send(self, topic: str, value: dict, key: str | None = None):
        await self._producer.send_and_wait(topic, value=value, key=key)