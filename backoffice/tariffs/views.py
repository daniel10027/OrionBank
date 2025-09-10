﻿from rest_framework import viewsets
from .models import Tariff
from .serializers import TariffSerializer

class TariffViewSet(viewsets.ModelViewSet):
    queryset = Tariff.objects.all()
    serializer_class = TariffSerializer