from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from core.app.api import accounts, transactions, health
from core.app.startup import lifespan
from core.app.config import settings

app = FastAPI(
    title=settings.app_name,
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router, prefix="/v1/health", tags=["Health"])
app.include_router(accounts.router, prefix="/v1/accounts", tags=["Accounts"])
app.include_router(transactions.router, prefix="/v1/transactions", tags=["Transactions"])