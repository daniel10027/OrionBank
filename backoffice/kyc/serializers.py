from rest_framework import serializers
from .models import KYCCase

class KYCCaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = KYCCase
        fields = "__all__"