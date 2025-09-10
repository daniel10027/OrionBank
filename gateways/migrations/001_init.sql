CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Webhook logs (optionnel pour audit)
CREATE TABLE IF NOT EXISTS webhook_logs (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  provider VARCHAR(64) NOT NULL, -- orionmoney, cardpsp, kyc
  signature VARCHAR(256),
  payload JSONB NOT NULL,
  received_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- Idempotency for gateway-initiated POSTs
CREATE TABLE IF NOT EXISTS idempotency_keys (
  key VARCHAR(128) PRIMARY KEY,
  fingerprint VARCHAR(128) NOT NULL,
  response JSONB,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  expire_at TIMESTAMPTZ NOT NULL
);

-- Outbox events (durable before Kafka)
CREATE TABLE IF NOT EXISTS outbox_events (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  topic VARCHAR(128) NOT NULL,
  key VARCHAR(128),
  payload JSONB NOT NULL,
  status VARCHAR(16) NOT NULL CHECK (status IN ('pending','sent','failed')) DEFAULT 'pending',
  attempt INT NOT NULL DEFAULT 0,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);
CREATE INDEX IF NOT EXISTS idx_outbox_status ON outbox_events(status);