import os
from dataclasses import dataclass

@dataclass
class Settings:
    app_name: str = os.getenv("APP_NAME", "Orion Gateways API")
    api_key: str = os.getenv("API_KEY", "change-me")

    db_user: str = os.getenv("DB_USER", "orion")
    db_password: str = os.getenv("DB_PASSWORD", "orion")
    db_host: str = os.getenv("DB_HOST", "localhost")
    db_port: int = int(os.getenv("DB_PORT", 5432))
    db_name: str = os.getenv("DB_NAME", "orion_gateways")

    kafka_bootstrap: str = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")
    kafka_client_id: str = os.getenv("KAFKA_CLIENT_ID", "gateways")
    kafka_dlq_topic: str = os.getenv("KAFKA_DLQ_TOPIC", "gateways.dlq")

    webhook_secret: str = os.getenv("WEBHOOK_SHARED_SECRET", "")
    webhook_skew: int = int(os.getenv("WEBHOOK_ALLOWED_SKEW_SECONDS", 300))

    orionmoney_base: str = os.getenv("ORION_MONEY_BASE_URL", "")
    orionmoney_key: str = os.getenv("ORION_MONEY_API_KEY", "")
    cardpsp_base: str = os.getenv("CARD_PSP_BASE_URL", "")
    cardpsp_key: str = os.getenv("CARD_PSP_API_KEY", "")
    kyc_base: str = os.getenv("KYC_BASE_URL", "")
    kyc_key: str = os.getenv("KYC_API_KEY", "")

    @property
    def db_dsn(self) -> str:
        return (
            f"postgresql+psycopg2://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"
        )

settings = Settings()