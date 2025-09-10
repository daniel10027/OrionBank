from flask import request
from . import card_bp
from ..middleware.auth import require_api_key
from ..services.card_psp_client import CardPspClient
from ..events.outbox import Outbox

@card_bp.post("/v1/gw/card/authorize")
def authorize():
    """Authorize a card transaction
    ---
    tags: [CardPSP]
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
              token: { type: string }
              amount: { type: string }
              currency: { type: string, default: XOF }
            required: [token, amount]
    """
    require_api_key()
    d = request.get_json(force=True)
    client = CardPspClient()
    res = client.authorize(token=d["token"], amount=d["amount"], currency=d.get("currency", "XOF"))
    Outbox.add(
        topic="transaction.initiated.v1",
        key=res["auth_id"],
        payload={"provider": "cardpsp", "auth_id": res["auth_id"], "amount": d["amount"]},
    )
    return res, 200