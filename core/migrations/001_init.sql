CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE IF NOT EXISTS accounts (
  id UUID PRIMARY KEY,
  customer_id UUID NOT NULL,
  type VARCHAR(16) NOT NULL CHECK (type IN ('current','savings','wallet')),
  status VARCHAR(16) NOT NULL CHECK (status IN ('active','suspended','closed')),
  balance_available NUMERIC(18,2) NOT NULL DEFAULT 0,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS transactions (
  id UUID PRIMARY KEY,
  account_debit UUID NOT NULL REFERENCES accounts(id),
  account_credit UUID NOT NULL REFERENCES accounts(id),
  amount NUMERIC(18,2) NOT NULL,
  charged_fee NUMERIC(18,2) NOT NULL DEFAULT 0,
  channel VARCHAR(16) NOT NULL CHECK (channel IN ('wallet','card','qr')),
  status VARCHAR(16) NOT NULL CHECK (status IN ('pending','settled','failed')),
  trace_id VARCHAR(64) NOT NULL,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_transactions_trace ON transactions(trace_id);

CREATE TABLE IF NOT EXISTS ledger_entries (
  id UUID PRIMARY KEY,
  tx_id UUID NOT NULL REFERENCES transactions(id),
  account_id UUID NOT NULL REFERENCES accounts(id),
  direction VARCHAR(8) NOT NULL CHECK (direction IN ('debit','credit')),
  amount NUMERIC(18,2) NOT NULL,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS fee_schedules (
  id UUID PRIMARY KEY,
  operation VARCHAR(32) NOT NULL, -- e.g. transfer_wallet
  channel VARCHAR(16) NOT NULL CHECK (channel IN ('wallet','card','qr')),
  fixed NUMERIC(18,2) NOT NULL DEFAULT 0,
  percent NUMERIC(5,2) NOT NULL DEFAULT 0
);

-- Idempotency store
CREATE TABLE IF NOT EXISTS idempotency_keys (
  key VARCHAR(128) PRIMARY KEY,
  fingerprint VARCHAR(128) NOT NULL,
  response JSONB,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  expire_at TIMESTAMPTZ NOT NULL
);

-- Outbox
CREATE TABLE IF NOT EXISTS outbox_events (
  id UUID PRIMARY KEY,
  topic VARCHAR(128) NOT NULL,
  key VARCHAR(128),
  payload JSONB NOT NULL,
  status VARCHAR(16) NOT NULL CHECK (status IN ('pending','sent','failed')) DEFAULT 'pending',
  attempt INT NOT NULL DEFAULT 0,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_outbox_status ON outbox_events(status);