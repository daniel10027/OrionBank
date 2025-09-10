import uuid
from decimal import Decimal
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from core.app.domain.repositories import AccountRepository, TransactionRepository, LedgerRepository, OutboxRepository
from core.app.domain.exceptions import AccountNotFound, InsufficientFunds, AccountClosed
from core.app.domain.models import Transaction

class TransferUseCase:
    def __init__(self, *, session: AsyncSession, accounts: AccountRepository, transactions: TransactionRepository, ledger: LedgerRepository, outbox: OutboxRepository, fee_engine, risk_rules):
        self.session = session
        self.accounts = accounts
        self.transactions = transactions
        self.ledger = ledger
        self.outbox = outbox
        self.fee_engine = fee_engine
        self.risk = risk_rules

    async def execute(self, *, debit: UUID, credit: UUID, amount: Decimal, channel: str, trace_id: str) -> dict:
        await self.risk.check_transfer(amount=amount, channel=channel)

        acc_debit = await self.accounts.get(debit)
        acc_credit = await self.accounts.get(credit)
        if not acc_debit or not acc_credit:
            raise AccountNotFound("Account not found")
        if acc_debit.status != "active" or acc_credit.status != "active":
            raise AccountClosed("Account is not active")
        if acc_debit.balance_available < amount:
            raise InsufficientFunds("Insufficient funds")

        fee = await self.fee_engine.compute("transfer_wallet", channel, amount)
        tx = Transaction(
            id=uuid.uuid4(),
            account_debit=debit,
            account_credit=credit,
            amount=amount,
            charged_fee=fee,
            channel=channel,
            status="pending",
            trace_id=trace_id,
        )

        # Persist TX
        await self.transactions.create(tx)
        await self.outbox.add_event(
            topic="transaction.initiated.v1",
            key=str(tx.id),
            payload={"transaction_id": str(tx.id), "amount": str(amount), "channel": channel, "trace_id": trace_id},
        )

        # Double-entry
        await self.ledger.add_entry(tx_id=tx.id, account_id=debit, direction="debit", amount=amount)
        await self.ledger.add_entry(tx_id=tx.id, account_id=credit, direction="credit", amount=amount - fee)

        # Apply balances
        await self.accounts.update_balance(debit, acc_debit.balance_available - amount)
        await self.accounts.update_balance(credit, acc_credit.balance_available + (amount - fee))

        # Mark settled + event
        await self.transactions.set_status(tx.id, "settled")
        await self.outbox.add_event(
            topic="transaction.settled.v1",
            key=str(tx.id),
            payload={
                "transaction_id": str(tx.id),
                "amount": str(amount),
                "charged_fee": str(fee),
                "debit_account": str(debit),
                "credit_account": str(credit),
                "channel": channel,
            },
        )

        await self.session.commit()
        return {"transaction_id": str(tx.id), "status": "settled", "charged_fee": str(fee)}