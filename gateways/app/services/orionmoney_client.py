from .http import get_session
from ..config import settings

class OrionMoneyClient:
    def __init__(self):
        self.base = settings.orionmoney_base.rstrip("/")
        self.key = settings.orionmoney_key
        self.sess = get_session()

    def initiate_payment(self, *, payer_msisdn: str, amount: str, currency: str = "XOF") -> dict:
        # Mock: in real life, call the PSP
        # r = self.sess.post(f"{self.base}/payments", headers={"Authorization": f"Bearer {self.key}"}, json={...})
        return {
            "payment_id": "pm_123",
            "status": "initiated",
            "redirect_url": "https://pay.example/pm_123",
        }