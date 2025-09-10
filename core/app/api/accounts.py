from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from core.app.infrastructure.db import get_session
from core.app.infrastructure.repositories import AccountRepositoryImpl
from core.app.schemas.account import AccountCreate, AccountResponse
from core.app.use_cases.create_account import CreateAccountUseCase
from core.app.use_cases.get_balance import GetBalanceUseCase
from uuid import UUID

router = APIRouter()

@router.post("/", response_model=AccountResponse)
async def create_account(payload: AccountCreate, session: AsyncSession = Depends(get_session)):
    uc = CreateAccountUseCase(session, AccountRepositoryImpl(session))
    return await uc.execute(payload)

@router.get("/{account_id}/balance", response_model=AccountResponse)
async def get_balance(account_id: UUID, session: AsyncSession = Depends(get_session)):
    acc_repo = AccountRepositoryImpl(session)
    uc = GetBalanceUseCase(acc_repo)
    try:
        return await uc.execute(account_id)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))