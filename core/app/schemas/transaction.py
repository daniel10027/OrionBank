from pydantic import BaseModel, UUID4, Field
from enum import Enum
from decimal import Decimal

class Channel(str, Enum):
    WALLET = "wallet"
    CARD = "card"
    QR = "qr"

class TransferRequest(BaseModel):
    account_debit: UUID4
    account_credit: UUID4
    amount: Decimal = Field(gt=0)
    channel: Channel

class TransferResponse(BaseModel):
    transaction_id: UUID4
    status: str
    charged_fee: Decimal