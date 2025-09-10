from flask import Blueprint

health_bp = Blueprint("health", __name__)
orionmoney_bp = Blueprint("orionmoney", __name__)
card_bp = Blueprint("card", __name__)
kyc_bp = Blueprint("kyc", __name__)