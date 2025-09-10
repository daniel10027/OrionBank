from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    app_name: str = Field("Orion Core Banking API", alias="APP_NAME")
    app_env: str = Field("dev", alias="APP_ENV")

    db_user: str = Field(..., alias="DB_USER")
    db_password: str = Field(..., alias="DB_PASSWORD")
    db_host: str = Field(..., alias="DB_HOST")
    db_port: int = Field(..., alias="DB_PORT")
    db_name: str = Field(..., alias="DB_NAME")

    kafka_bootstrap: str = Field(..., alias="KAFKA_BOOTSTRAP_SERVERS")
    kafka_client_id: str = Field("core-banking", alias="KAFKA_CLIENT_ID")
    kafka_outbox_topic: str = Field("core.outbox.events", alias="KAFKA_OUTBOX_TOPIC")
    kafka_dlq_topic: str = Field("core.outbox.dlq", alias="KAFKA_DLQ_TOPIC")

    idempotency_ttl_seconds: int = Field(86400, alias="IDEMPOTENCY_TTL_SECONDS")

    @property
    def db_dsn(self) -> str:
        return (
            f"postgresql+asyncpg://{self.db_user}:{self.db_password}@"
            f"{self.db_host}:{self.db_port}/{self.db_name}"
        )

settings = Settings(_env_file=".env", _env_file_encoding="utf-8")