from decimal import Decimal

class RiskRules:
    async def check_transfer(self, *, amount: Decimal, channel: str) -> None:
        # Exemples de règles simples (placeholders)
        if amount <= 0:
            raise ValueError("Amount must be > 0")
        if channel not in {"wallet", "card", "qr"}:
            raise ValueError("Invalid channel")
        # Ajouter velocity checks, device fingerprint, sanctions... si besoin