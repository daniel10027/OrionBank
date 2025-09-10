from uuid import UUID, uuid4
from decimal import Decimal
from typing import Optional
from sqlalchemy import select, update, func, literal
from sqlalchemy.ext.asyncio import AsyncSession
from core.app.domain.models import Account, Transaction
from core.app.domain.repositories import (
    AccountRepository, TransactionRepository, LedgerRepository, OutboxRepository, IdempotencyRepository
)
from .models import AccountORM, TransactionORM, LedgerEntryORM, OutboxEventORM, IdempotencyKeyORM
from datetime import timedelta
from dateutil import tz
from datetime import datetime

class AccountRepositoryImpl(AccountRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get(self, account_id: UUID) -> Optional[Account]:
        row = await self.session.get(AccountORM, account_id)
        if not row:
            return None
        return Account(
            id=row.id,
            customer_id=row.customer_id,
            type=row.type,
            status=row.status,
            balance_available=Decimal(row.balance_available),
        )

    async def create(self, account: Account) -> Account:
        row = AccountORM(
            id=account.id,
            customer_id=account.customer_id,
            type=account.type,
            status=account.status,
            balance_available=account.balance_available,
        )
        self.session.add(row)
        await self.session.flush()
        return account

    async def update_balance(self, account_id: UUID, new_balance: Decimal) -> None:
        await self.session.execute(
            update(AccountORM).where(AccountORM.id == account_id).values(balance_available=new_balance)
        )

class TransactionRepositoryImpl(TransactionRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, tx: Transaction) -> Transaction:
        row = TransactionORM(
            id=tx.id,
            account_debit=tx.account_debit,
            account_credit=tx.account_credit,
            amount=tx.amount,
            charged_fee=tx.charged_fee,
            channel=tx.channel,
            status=tx.status,
            trace_id=tx.trace_id,
        )
        self.session.add(row)
        await self.session.flush()
        return tx

    async def set_status(self, tx_id: UUID, status: str) -> None:
        await self.session.execute(
            update(TransactionORM).where(TransactionORM.id == tx_id).values(status=status)
        )

class LedgerRepositoryImpl(LedgerRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add_entry(self, *, tx_id: UUID, account_id: UUID, direction: str, amount: Decimal) -> None:
        row = LedgerEntryORM(tx_id=tx_id, account_id=account_id, direction=direction, amount=amount)
        self.session.add(row)

class OutboxRepositoryImpl(OutboxRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add_event(self, topic: str, key: str | None, payload: dict) -> None:
        row = OutboxEventORM(id=uuid4(), topic=topic, key=key, payload=payload, status="pending", attempt=0)
        self.session.add(row)

class IdempotencyRepositoryImpl(IdempotencyRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def put(self, *, key: str, fingerprint: str, response: dict, ttl_seconds: int) -> None:
        expire_at = datetime.utcnow() + timedelta(seconds=ttl_seconds)
        row = IdempotencyKeyORM(key=key, fingerprint=fingerprint, response=response, expire_at=expire_at)
        self.session.merge(row)

    async def get(self, *, key: str, fingerprint: str) -> Optional[dict]:
        row = await self.session.get(IdempotencyKeyORM, key)
        if row and row.fingerprint == fingerprint and row.expire_at > datetime.utcnow():
            return row.response
        return None