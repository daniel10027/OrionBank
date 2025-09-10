from django.contrib import admin
from .models import KYCCase

@admin.register(KYCCase)
class KYCCaseAdmin(admin.ModelAdmin):
    list_display = ("id", "customer_id", "document_no", "status", "created_at")
    list_filter = ("status",)
    search_fields = ("customer_id", "document_no")