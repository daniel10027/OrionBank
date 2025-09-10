from sqlalchemy import text
from ..db import db_session

OUTBOX_INSERT = text("""
    INSERT INTO outbox_events (topic, key, payload, status, attempt)
    VALUES (:topic, :key, CAST(:payload AS JSONB), 'pending', 0)
""")

OUTBOX_SELECT = text("""
    SELECT id, topic, key, payload::text FROM outbox_events
    WHERE status = 'pending' ORDER BY created_at LIMIT 100
""")

OUTBOX_MARK = text("""
    UPDATE outbox_events SET status = :status, attempt = attempt + 1 WHERE id = :id
""")

class Outbox:
    @staticmethod
    def add(topic: str, key: str | None, payload: dict) -> None:
        import json
        with db_session() as s:
            s.execute(OUTBOX_INSERT, {"topic": topic, "key": key, "payload": json.dumps(payload)})

    @staticmethod
    def drain(producer):
        # Poll and push to Kafka
        with db_session() as s:
            rows = s.execute(OUTBOX_SELECT).mappings().all()
            for r in rows:
                try:
                    import json
                    payload = json.loads(r["payload"]) if isinstance(r["payload"], str) else r["payload"]
                    producer.send(r["topic"], payload, key=r["key"])
                    s.execute(OUTBOX_MARK, {"status": "sent", "id": r["id"]})
                except Exception:
                    s.execute(OUTBOX_MARK, {"status": "failed", "id": r["id"]})