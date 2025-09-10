from . import health_bp

@health_bp.get("/v1/health")
def health():
    return {"status": "ok"}