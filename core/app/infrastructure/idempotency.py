import hashlib
from fastapi import Request

def request_fingerprint(request: Request, body_bytes: bytes) -> str:
    # Construit une empreinte stable de la requête (méthode + path + body)
    h = hashlib.sha256()
    h.update(request.method.encode())
    h.update(request.url.path.encode())
    h.update(body_bytes)
    return h.hexdigest()