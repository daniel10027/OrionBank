from flask import Flask
from flasgger import Swagger
from .routes.health import health_bp
from .routes.orionmoney import orionmoney_bp
from .routes.card_psp import card_bp
from .routes.kyc import kyc_bp
from .events.producer import producer
from .events.outbox import Outbox
import threading, time

SWAGGER_TEMPLATE = {
    "swagger": "2.0",
    "info": {"title": "Orion Gateways API", "version": "1.0.0"},
}


def create_app() -> Flask:
    app = Flask(__name__)
    Swagger(app, template=SWAGGER_TEMPLATE)

    # Blueprints
    app.register_blueprint(health_bp)
    app.register_blueprint(orionmoney_bp)
    app.register_blueprint(card_bp)
    app.register_blueprint(kyc_bp)

    # Start Kafka producer and outbox drainer
    producer.start()

    def outbox_loop():
        while True:
            try:
                Outbox.drain(producer)
            except Exception:
                pass
            time.sleep(0.5)

    threading.Thread(target=outbox_loop, daemon=True).start()

    return app