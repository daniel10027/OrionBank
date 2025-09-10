from pydantic import BaseModel, UUID4, Field
from enum import Enum
from decimal import Decimal

class AccountType(str, Enum):
    CURRENT = "current"
    SAVINGS = "savings"
    WALLET = "wallet"

class AccountStatus(str, Enum):
    ACTIVE = "active"
    SUSPENDED = "suspended"
    CLOSED = "closed"

class AccountCreate(BaseModel):
    customer_id: UUID4
    type: AccountType

class AccountResponse(BaseModel):
    id: UUID4
    customer_id: UUID4
    type: AccountType
    status: AccountStatus
    balance_available: Decimal