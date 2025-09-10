from django.contrib import admin
from .models import Dispute

@admin.register(Dispute)
class DisputeAdmin(admin.ModelAdmin):
    list_display = ("id", "transaction_id", "status", "created_at")
    list_filter = ("status",)
    search_fields = ("transaction_id",)