from uuid import UUID
from core.app.domain.repositories import AccountRepository
from core.app.domain.exceptions import AccountNotFound
from core.app.schemas.account import AccountResponse, AccountStatus

class GetBalanceUseCase:
    def __init__(self, accounts: AccountRepository):
        self.accounts = accounts

    async def execute(self, account_id: UUID) -> AccountResponse:
        acc = await self.accounts.get(account_id)
        if not acc:
            raise AccountNotFound("Account not found")
        return AccountResponse(
            id=acc.id,
            customer_id=acc.customer_id,
            type=acc.type,  # type: ignore
            status=AccountStatus(acc.status),
            balance_available=acc.balance_available,
        )