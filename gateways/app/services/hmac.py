import hmac
import hashlib
import base64
from datetime import datetime, timezone
from dateutil import parser
from ..config import settings

HEADER_SIG = "X-Signature"
HEADER_TS = "X-Timestamp"

def compute_signature(body: bytes, timestamp: str, secret: str) -> str:
    msg = timestamp.encode() + b"." + body
    digest = hmac.new(secret.encode(), msg, hashlib.sha256).digest()
    return base64.b64encode(digest).decode()

class WebhookVerifier:
    @staticmethod
    def verify(body: bytes, headers: dict) -> None:
        sig = headers.get(HEADER_SIG)
        ts = headers.get(HEADER_TS)
        if not sig or not ts:
            raise ValueError("Missing signature headers")
        try:
            ts_dt = parser.isoparse(ts)
        except Exception:
            raise ValueError("Invalid timestamp")
        now = datetime.now(timezone.utc)
        skew = abs((now - ts_dt).total_seconds())
        if skew > settings.webhook_skew:
            raise ValueError("Timestamp skew too large")
        expected = compute_signature(body, ts, settings.webhook_secret)
        if not hmac.compare_digest(expected, sig):
            raise ValueError("Invalid signature")