# Orion Backoffice (Django)

## Setup

```bash

cp .env.example .env
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver 0.0.0.0:8001
````

## Endpoints

* Admin: `/admin/`
* API Docs: `/api/docs/`
* Redoc: `/api/redoc/`
* KYC Cases: `/api/kyc/cases/`
* Disputes: `/api/disputes/cases/`
* Reporting: `/api/reporting/transactions/`
* Tariffs: `/api/tariffs/`