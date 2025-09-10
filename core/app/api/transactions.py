from fastapi import APIRouter, Depends, Header, HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession
from core.app.infrastructure.db import get_session
from core.app.infrastructure.repositories import (
    AccountRepositoryImpl, TransactionRepositoryImpl, LedgerRepositoryImpl, OutboxRepositoryImpl
)
from core.app.infrastructure.fees import FeeEngine
from core.app.infrastructure.risk import RiskRules
from core.app.infrastructure.idempotency import request_fingerprint
from core.app.infrastructure.models import IdempotencyKeyORM
from core.app.schemas.transaction import TransferRequest, TransferResponse
from core.app.use_cases.transfer import TransferUseCase
from core.app.config import settings
from sqlalchemy import select
from datetime import datetime, timezone

router = APIRouter()

@router.post("/transfer", response_model=TransferResponse)
async def transfer(
    payload: TransferRequest,
    request: Request,
    session: AsyncSession = Depends(get_session),
    idempotency_key: str | None = Header(default=None, alias="Idempotency-Key"),
):
    # Idempotence guard (key + request fingerprint)
    body = await request.body()
    fp = request_fingerprint(request, body)

    if idempotency_key:
        prev = await session.get(IdempotencyKeyORM, idempotency_key)
        if prev and prev.fingerprint == fp and prev.expire_at > datetime.now(timezone.utc):
            data = prev.response
            return TransferResponse(**data)

    uc = TransferUseCase(
        session=session,
        accounts=AccountRepositoryImpl(session),
        transactions=TransactionRepositoryImpl(session),
        ledger=LedgerRepositoryImpl(session),
        outbox=OutboxRepositoryImpl(session),
        fee_engine=FeeEngine(session),
        risk_rules=RiskRules(),
    )
    try:
        result = await uc.execute(
            debit=payload.account_debit,
            credit=payload.account_credit,
            amount=payload.amount,
            channel=payload.channel.value,
            trace_id=idempotency_key or "trace-" + fp[:16],
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    response_obj = TransferResponse(
        transaction_id=result["transaction_id"],
        status=result["status"],
        charged_fee=result["charged_fee"],
    )

    if idempotency_key:
        from datetime import timedelta
        expire_at = datetime.now(timezone.utc) + timedelta(seconds=settings.idempotency_ttl_seconds)
        key_row = IdempotencyKeyORM(
            key=idempotency_key,
            fingerprint=fp,
            response=response_obj.model_dump(),
            expire_at=expire_at,
        )
        session.merge(key_row)
        await session.commit()

    return response_obj