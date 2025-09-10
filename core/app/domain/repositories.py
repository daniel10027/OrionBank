from abc import ABC, abstractmethod
from typing import Optional
from uuid import UUID
from decimal import Decimal
from .models import Account, Transaction

class AccountRepository(ABC):
    @abstractmethod
    async def get(self, account_id: UUID) -> Optional[Account]: ...

    @abstractmethod
    async def create(self, account: Account) -> Account: ...

    @abstractmethod
    async def update_balance(self, account_id: UUID, new_balance: Decimal) -> None: ...

class TransactionRepository(ABC):
    @abstractmethod
    async def create(self, tx: Transaction) -> Transaction: ...

    @abstractmethod
    async def set_status(self, tx_id: UUID, status: str) -> None: ...

class LedgerRepository(ABC):
    @abstractmethod
    async def add_entry(self, *, tx_id: UUID, account_id: UUID, direction: str, amount: Decimal) -> None: ...

class OutboxRepository(ABC):
    @abstractmethod
    async def add_event(self, topic: str, key: str | None, payload: dict) -> None: ...

class IdempotencyRepository(ABC):
    @abstractmethod
    async def put(self, *, key: str, fingerprint: str, response: dict, ttl_seconds: int) -> None: ...

    @abstractmethod
    async def get(self, *, key: str, fingerprint: str) -> Optional[dict]: ...