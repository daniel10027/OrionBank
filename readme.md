# Cahier des Charges – Écosystème Orion Bank  
**Stack : Django + Flask + FastAPI + Apache Kafka**  
**Architecture microservices & événements**

---

## 1. Contexte & Objectifs

**Contexte :**  
Orion Bank souhaite une plateforme **scalable**, **sécurisée** et **événementielle** pour gérer comptes, paiements, KYC/AML et reporting temps réel.

**Objectifs :**
- Architecture **microservices** avec interactions asynchrones via **Kafka**.
- Séparation claire :
  - **FastAPI** → Core Banking.
  - **Flask** → Gateways & intégrations.
  - **Django** → Back-office & admin.
- Résilience, observabilité, conformité **PCI-DSS/AML**.
- Temps réel : notifications, anti-fraude, reporting.

---

## 2. Périmètre Fonctionnel

1. **Gestion des clients & KYC**
   - Enrôlement, vérification identité, niveaux KYC.
   - Statuts : `pending` / `verified` / `rejected`.
2. **Comptes & Wallets**
   - Comptes courants, épargne, wallets virtuels.
3. **Transactions**
   - Dépôt, retrait, transfert P2P, paiement marchand.
   - Idempotence, compensation, réconciliation.
4. **Moyens de paiement**
   - **Orion Money**, cartes, QR code.
5. **Tarification & Fees**
   - Frais dynamiques par type d’opération.
6. **Conformité AML/CFT**
   - Scoring, seuils, alertes, audits.
7. **Support & Litiges**
   - Gestion des chargebacks et remboursements.
8. **Reporting & BI**
   - Dashboards temps réel, exports, agrégats.
9. **Notifications**
   - Email, SMS, Push.

---

## 3. Architecture Cible

### Macro-composition

- **FastAPI — Core Banking Services**
  - Comptes, transactions, ledger, anti-fraude.
- **Flask — Gateways**
  - Orion Money, PSP cartes, opérateurs tiers.
- **Django — Back-office**
  - Admin, KYC, litiges, reporting.

### Communication

- REST/gRPC pour appels directs.
- **Kafka** pour événements métier.
- Base de données **par service**.

### Topologie

- Environnements séparés : dev, staging, prod.
- API Gateway + Service Mesh (optionnel).
- Sécurité via WAF, secrets via Vault.

---

## 4. Décomposition des Services

### 4.1 FastAPI — Core Banking

- **Account Service** : création, gestion, limites.
- **Ledger Service** : double écriture comptable.
- **Transaction Service** : orchestration transferts/P2P.
- **Fee Engine** : calcul automatique des frais.
- **Risk & Rules** : scoring, alertes anti-fraude.
- **Notification Orchestrator** : événements `transaction.completed`.

### 4.2 Flask — Gateways

- **Orion Money Gateway** : initier paiements, webhooks sécurisés.
- **Card PSP Gateway** : tokenisation, autorisation, refunds.
- **KYC/AML Gateway** : OCR, screening sanctions.
- **BillPay Gateway** : factures, marchands.

### 4.3 Django — Back-office

- **Admin Ops** : gestion opérateurs, permissions RBAC.
- **KYC Console** : vérification manuelle des dossiers.
- **Litiges** : gestion des chargebacks.
- **Tarification** : CRUD des barèmes.
- **Reporting** : dashboards & exports.

---

## 5. Modèle de Données (extraits)

### Account
| Champ | Type | Description |
|-------|------|------------|
| `id` | UUID | Identifiant compte |
| `customer_id` | UUID | Référence client |
| `type` | ENUM | Courant, épargne, wallet |
| `status` | ENUM | Active, suspendue, fermée |
| `balance_available` | Decimal | Solde dispo |

### Transaction
| Champ | Type | Description |
|-------|------|------------|
| `id` | UUID | Identifiant unique |
| `account_debit` | UUID | Compte débité |
| `account_credit` | UUID | Compte crédité |
| `amount` | Decimal | Montant transaction |
| `status` | ENUM | pending, settled, failed |
| `channel` | ENUM | wallet, card, qr |

---

## 6. Kafka & Événements

### Topics Métier

- `customer.created.v1`
- `kyc.updated.v1`
- `account.opened.v1`
- `transaction.initiated.v1`
- `transaction.settled.v1`
- `transaction.failed.v1`
- `webhook.Orionmoney.payment.v1`

### Schéma Avro Exemple

```json
{
  "type": "record",
  "name": "TransactionSettled",
  "namespace": "Orion.bank",
  "fields": [
    {"name": "transaction_id", "type": "string"},
    {"name": "amount", "type": "string"},
    {"name": "currency", "type": "string"},
    {"name": "channel", "type": "string"},
    {"name": "charged_fee", "type": "string"},
    {"name": "debit_account", "type": "string"},
    {"name": "credit_account", "type": "string"},
    {"name": "settled_at", "type": "string"}
  ]
}
````

### Bonnes Pratiques Kafka

* **Outbox Pattern** pour cohérence DB/événements.
* **Idempotence** via clés.
* **DLQ** pour erreurs.
* **Schema Registry** pour compatibilité ascendante.

---

## 7. APIs (extraits)

### FastAPI (Core)

```
POST /v1/accounts
POST /v1/transactions/transfer
GET /v1/accounts/{id}/balance
GET /v1/transactions/{id}
```

### Flask (Gateways)

```
POST /v1/gw/Orionmoney/initiate
POST /v1/gw/Orionmoney/webhook
POST /v1/gw/card/authorize
```

### Django (Back-office)

```
GET /admin/kyc/cases
POST /admin/kyc/{case_id}/decision
GET /admin/reports/transactions
```

---

## 8. Sécurité & Conformité

* **TLS 1.2+** partout.
* **Secrets** gérés via Vault.
* **RBAC** par service et utilisateur.
* **Journaux d’audit immuables**.
* **PCI-DSS** : pas de stockage PAN, tokenisation.
* **KYC/AML** : screening automatique, audit trail complet.
* **Protection fraude** : règles velocity, device fingerprint.

---

## 9. Exigences Non-Fonctionnelles

| Exigence               | Objectif                             |
| ---------------------- | ------------------------------------ |
| **Disponibilité**      | 99.9%                                |
| **Latence API**        | p95 ≤ 200 ms                         |
| **Latence événements** | ≤ 1s                                 |
| **Débit**              | 200 TPS                              |
| **RPO/RTO**            | RPO ≤ 5 min / RTO ≤ 30 min           |
| **Observabilité**      | Prometheus + Grafana + OpenTelemetry |

---

## 10. Observabilité & Exploitation

* **Logs** : JSON → ELK/OpenSearch.
* **Metrics** : Prometheus (latence, Kafka lag, TPS).
* **Traces** : OpenTelemetry (Jaeger).
* **Alertes** : basées sur SLOs.
* **Dashboards** : temps réel, matérialisés via Kafka.

---

## 11. CI/CD & Qualité

* **CI** :

  * Lint : Ruff/Flake8.
  * Typage : MyPy.
  * Tests unitaires & intégration.
* **CD** :

  * Docker + Helm/Kustomize.
  * Scans vulnérabilités (Trivy).
* **Environnements** : dev, staging, prod.
* **Tests** :

  * Unitaires (≥70%).
  * Intégration Kafka/DB.
  * Contrats inter-services.
  * E2E en staging.

---

## 12. Flux Critiques (Exemple)

**Paiement marchand via Orion Money :**

1. Front → `POST /gw/Orionmoney/initiate`.
2. Flask initie paiement OM → publie `transaction.initiated`.
3. Webhook OM → Flask → publie `webhook.Orionmoney.payment`.
4. FastAPI consomme, applique SAGA : débite wallet, crédite marchand.
5. Django Back-office met à jour dashboards.
6. Notification SMS/Email via Kafka.

---

## 13. Patterns & Bonnes Pratiques

* **SAGA orchestration** pour transactions multi-comptes.
* **Idempotence** stricte.
* **Outbox Pattern** pour cohérence DB/Kafka.
* **Versionnement événements** : `.v1`, `.v2`.
* **Feature flags** pour déploiements progressifs.
* **Déploiements** : blue-green/canary.

---

## 14. Planning Macro

| Phase                | Durée  | Livrables                          |
| -------------------- | ------ | ---------------------------------- |
| Cadrage              | 2 sem. | Spécifications détaillées          |
| Fondations           | 3 sem. | CI/CD, Kafka topics, observabilité |
| Core Banking         | 6 sem. | FastAPI + Ledger + Transactions    |
| Gateways             | 5 sem. | Intégration OM, cartes, KYC        |
| Back-office          | 5 sem. | Django Admin, dashboards           |
| Conformité           | 3 sem. | Règles AML & fraude                |
| Tests & Durcissement | 3 sem. | E2E, sécurité                      |
| Go-Live              | 2 sem. | Déploiement progressif             |

---

## 15. Backlog Initial (Exemples)

* **Core Banking** : comptes, ledger, transferts.
* **Gateways** : init OM, webhooks, retries.
* **KYC** : screening, workflow validation.
* **Reporting** : exports CSV/XLSX.
* **Sécurité** : RBAC, audit, gestion secrets.

---

## 16. Critères d’Acceptation

* Transactions idempotentes.
* SAGA cohérent même en cas de timeout PSP.
* Événements publiés en ≤ 1s.
* Back-office affiche transactions < 2s.
* Traçabilité complète par `trace_id`.

---

## 17. Annexes Techniques

### 17.1 En-têtes Idempotence

```
POST /v1/transactions/transfer
Idempotency-Key: 9f1c-...
```

### 17.2 Signature HMAC Webhook

* `X-Signature: HMAC-SHA256(base64(payload), secret)`
* Horodatage ≤ ±5 min.

### 17.3 Politique Kafka

* Topics : `retention.ms=7d`, `cleanup.policy=compact`.
* DLQ : `retention.ms=30d`.

---

## 18. Livrables

* **Spécifications OpenAPI**.
* **Schémas Avro + Registry**.
* **Dockerfiles + Helm Charts**.
* **Jeux de tests unitaires & intégration**.
* **Dossier sécurité** : RBAC, PCI-DSS, PII.
* **Runbooks & Playbooks**.
