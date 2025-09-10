from decimal import Decimal
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from .models import FeeScheduleORM

class FeeEngine:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def compute(self, operation: str, channel: str, amount: Decimal) -> Decimal:
        q = select(FeeScheduleORM).where(
            FeeScheduleORM.operation == operation, FeeScheduleORM.channel == channel
        )
        row = (await self.session.execute(q)).scalar_one_or_none()
        if not row:
            return Decimal("0")
        fee = Decimal(row.fixed) + (Decimal(row.percent) / Decimal("100")) * amount
        return fee.quantize(Decimal("0.01"))