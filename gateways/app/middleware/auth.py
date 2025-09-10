from flask import request, abort
from ..config import settings

def require_api_key():
    key = request.headers.get("X-API-Key")
    if not key or key != settings.api_key:
        abort(401, description="Unauthorized")