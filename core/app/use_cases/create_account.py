import uuid
from decimal import Decimal
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from core.app.domain.models import Account
from core.app.domain.repositories import AccountRepository
from core.app.schemas.account import AccountCreate, AccountResponse, AccountStatus

class CreateAccountUseCase:
    def __init__(self, session: AsyncSession, accounts: AccountRepository):
        self.session = session
        self.accounts = accounts

    async def execute(self, payload: AccountCreate) -> AccountResponse:
        account = Account(
            id=uuid.uuid4(),
            customer_id=payload.customer_id,
            type=payload.type.value,
            status=AccountStatus.ACTIVE.value,
            balance_available=Decimal("0.00"),
        )
        await self.accounts.create(account)
        await self.session.commit()
        return AccountResponse(
            id=account.id,
            customer_id=account.customer_id,
            type=payload.type,
            status=AccountStatus.ACTIVE,
            balance_available=Decimal("0.00"),
        )