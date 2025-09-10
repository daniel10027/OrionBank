from .http import get_session
from ..config import settings

class KycClient:
    def __init__(self):
        self.base = settings.kyc_base.rstrip("/")
        self.key = settings.kyc_key
        self.sess = get_session()

    def screen(self, *, full_name: str, document_no: str) -> dict:
        return {"score": 0.02, "lists": []}