from .http import get_session
from ..config import settings

class CardPspClient:
    def __init__(self):
        self.base = settings.cardpsp_base.rstrip("/")
        self.key = settings.cardpsp_key
        self.sess = get_session()

    def authorize(self, *, token: str, amount: str, currency: str = "XOF") -> dict:
        return {"auth_id": "auth_789", "status": "approved"}