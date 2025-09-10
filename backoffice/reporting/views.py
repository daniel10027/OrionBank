from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(["GET"])
def transactions_report(request):
    # Placeholder: in real life, query DB or Kafka materialized view
    data = {
        "total_volume": "1000000",
        "currency": "XOF",
        "count": 1234,
    }
    return Response(data)