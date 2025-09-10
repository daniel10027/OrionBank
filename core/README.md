# Orion Core Banking (FastAPI)

## Prérequis
- Python 3.11+
- PostgreSQL 14+
- Kafka (Bootstrap servers)

## Setup
```bash
cp .env.example .env
# éditez .env

# Créez la base de données et appliquez la migration
psql -h $DB_HOST -U $DB_USER -d $DB_NAME -f migrations/001_init.sql

# Démarrez l'API
uvicorn app.main:app --reload
````

## Endpoints

* Swagger: `/docs`
* ReDoc: `/redoc`

## Idempotence

* Utilisez l'en-tête `Idempotency-Key: <uuid>` sur `POST /v1/transactions/transfer`.

## Événements (Outbox)

* Les événements sont insérés dans `outbox_events` et envoyés vers Kafka en tâche de fond.


## 🧪 Notes & Extensions

* Pour la **consommation Kafka** (anti-fraude, projections, notifications), on l’implémentera dans les autres microservices.
* Ajoutez OpenTelemetry (OTLP) en instrumentant `app.main` si vous avez un collector.
* Ajoutez des **constraints de solde** via `SELECT ... FOR UPDATE` si vous souhaitez des verrous explicites (à ajouter).
* Des **tests d’intégration** complets peuvent être ajoutés (pytest/HTTPX + DB éphémère), mais ici on fournit le squelette prêt à brancher.
