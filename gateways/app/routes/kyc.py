from flask import request
from . import kyc_bp
from ..middleware.auth import require_api_key
from ..services.kyc_client import KycClient
from ..events.outbox import Outbox

@kyc_bp.post("/v1/gw/kyc/screen")
def screen():
    """KYC Screening
    ---
    tags: [KYC]
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
              full_name: { type: string }
              document_no: { type: string }
            required: [full_name, document_no]
    """
    require_api_key()
    d = request.get_json(force=True)
    c = KycClient()
    r = c.screen(full_name=d["full_name"], document_no=d["document_no"])
    Outbox.add(topic="kyc.updated.v1", key=d["document_no"], payload={"result": r, "subject": d})
    return r, 200