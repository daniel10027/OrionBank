from dataclasses import dataclass
from uuid import UUID
from decimal import Decimal

@dataclass
class Account:
    id: UUID
    customer_id: UUID
    type: str  # current | savings | wallet
    status: str  # active | suspended | closed
    balance_available: Decimal

@dataclass
class Transaction:
    id: UUID
    account_debit: UUID
    account_credit: UUID
    amount: Decimal
    charged_fee: Decimal
    channel: str  # wallet | card | qr
    status: str   # pending | settled | failed
    trace_id: str