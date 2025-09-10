import json
from flask import request, abort
from . import orionmoney_bp
from ..middleware.auth import require_api_key
from ..services.hmac import WebhookVerifier, HEADER_SIG, HEADER_TS
from ..services.orionmoney_client import OrionMoneyClient
from ..events.outbox import Outbox

@orionmoney_bp.post("/v1/gw/orionmoney/initiate")
def initiate_payment():
    """Initiate a payment via Orion Money
    ---
    tags: [OrionMoney]
    parameters:
      - in: header
        name: X-API-Key
        required: true
        schema: { type: string }
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            properties:
              payer_msisdn: { type: string }
              amount: { type: string }
              currency: { type: string, default: XOF }
            required: [payer_msisdn, amount]
    responses:
      200:
        description: Initiated
    """
    require_api_key()
    data = request.get_json(force=True)
    client = OrionMoneyClient()
    result = client.initiate_payment(
        payer_msisdn=data["payer_msisdn"], amount=data["amount"], currency=data.get("currency", "XOF")
    )
    # Publish business event
    Outbox.add(
        topic="transaction.initiated.v1",
        key=result["payment_id"],
        payload={
            "provider": "orionmoney",
            "payment_id": result["payment_id"],
            "amount": data["amount"],
            "currency": data.get("currency", "XOF"),
        },
    )
    return result, 200

@orionmoney_bp.post("/v1/gw/orionmoney/webhook")
def webhook():
    """Webhook Orion Money (signed HMAC)
    ---
    tags: [OrionMoney]
    parameters:
      - in: header
        name: X-Timestamp
        schema: { type: string }
      - in: header
        name: X-Signature
        schema: { type: string }
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            properties:
              payment_id: { type: string }
              status: { type: string }
              amount: { type: string }
              currency: { type: string }
    responses:
      200:
        description: Accepted
    """
    raw = request.get_data()
    try:
        WebhookVerifier.verify(raw, request.headers)
    except Exception as e:
        abort(400, description=str(e))

    payload = request.get_json(force=True)

    # Persist to outbox for downstream consumers
    Outbox.add(
        topic="webhook.Orionmoney.payment.v1",
        key=str(payload.get("payment_id")),
        payload=payload,
    )
    return {"status": "accepted"}, 200