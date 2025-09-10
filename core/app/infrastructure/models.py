import uuid
from sqlalchemy import Column, String, Numeric, CheckConstraint, ForeignKey, Integer
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func
from sqlalchemy.types import TIMESTAMP
from .db import Base

class AccountORM(Base):
    __tablename__ = "accounts"
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    customer_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    type: Mapped[str] = mapped_column(String(16), nullable=False)
    status: Mapped[str] = mapped_column(String(16), nullable=False)
    balance_available: Mapped[str] = mapped_column(Numeric(18,2), nullable=False, default=0)
    created_at: Mapped = mapped_column(TIMESTAMP(timezone=True), server_default=func.now())
    updated_at: Mapped = mapped_column(TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now())

class TransactionORM(Base):
    __tablename__ = "transactions"
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    account_debit: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("accounts.id"), nullable=False)
    account_credit: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("accounts.id"), nullable=False)
    amount: Mapped[str] = mapped_column(Numeric(18,2), nullable=False)
    charged_fee: Mapped[str] = mapped_column(Numeric(18,2), nullable=False, default=0)
    channel: Mapped[str] = mapped_column(String(16), nullable=False)
    status: Mapped[str] = mapped_column(String(16), nullable=False)
    trace_id: Mapped[str] = mapped_column(String(64), nullable=False)
    created_at: Mapped = mapped_column(TIMESTAMP(timezone=True), server_default=func.now())
    updated_at: Mapped = mapped_column(TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now())

class LedgerEntryORM(Base):
    __tablename__ = "ledger_entries"
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tx_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("transactions.id"), nullable=False)
    account_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("accounts.id"), nullable=False)
    direction: Mapped[str] = mapped_column(String(8), nullable=False)
    amount: Mapped[str] = mapped_column(Numeric(18,2), nullable=False)
    created_at: Mapped = mapped_column(TIMESTAMP(timezone=True), server_default=func.now())

class FeeScheduleORM(Base):
    __tablename__ = "fee_schedules"
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    operation: Mapped[str] = mapped_column(String(32), nullable=False)
    channel: Mapped[str] = mapped_column(String(16), nullable=False)
    fixed: Mapped[str] = mapped_column(Numeric(18,2), nullable=False, default=0)
    percent: Mapped[str] = mapped_column(Numeric(5,2), nullable=False, default=0)

class IdempotencyKeyORM(Base):
    __tablename__ = "idempotency_keys"
    key = Column(String(128), primary_key=True)
    fingerprint = Column(String(128), nullable=False)
    response = Column(JSONB)
    created_at = mapped_column(TIMESTAMP(timezone=True), server_default=func.now())
    expire_at = mapped_column(TIMESTAMP(timezone=True), nullable=False)

class OutboxEventORM(Base):
    __tablename__ = "outbox_events"
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    topic: Mapped[str] = mapped_column(String(128), nullable=False)
    key: Mapped[str | None] = mapped_column(String(128))
    payload = Column(JSONB, nullable=False)
    status: Mapped[str] = mapped_column(String(16), nullable=False, default="pending")
    attempt: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    created_at: Mapped = mapped_column(TIMESTAMP(timezone=True), server_default=func.now())
    updated_at: Mapped = mapped_column(TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now())