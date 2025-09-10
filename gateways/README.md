# Orion Gateways (Flask)

## Prérequis
- Python 3.11+
- PostgreSQL 14+
- Kafka

## Setup
```bash
cp .env.example .env
# Créez la base et exécutez la migration
psql -h $DB_HOST -U $DB_USER -d $DB_NAME -f migrations/001_init.sql

# Lancez en dev
export FLASK_APP=app.wsgi:app
flask run --port 7000

# Swagger
# http://localhost:7000/apidocs
````

## Sécurité Webhook

* Envoyez `X-Timestamp` (ISO8601 UTC) et `X-Signature = base64(HMAC_SHA256(ts + '.' + body))`.

## Outbox

* Les routes écrivent dans `outbox_events`. Un thread de fond publie sur Kafka.
