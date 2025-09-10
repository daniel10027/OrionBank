from rest_framework import viewsets
from .models import KYCCase
from .serializers import KYCCaseSerializer

class KYCCaseViewSet(viewsets.ModelViewSet):
    queryset = KYCCase.objects.all().order_by("-created_at")
    serializer_class = KYCCaseSerializer