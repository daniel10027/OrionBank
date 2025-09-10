from django.contrib import admin
from .models import Tariff

@admin.register(Tariff)
class TariffAdmin(admin.ModelAdmin):
    list_display = ("id", "operation", "channel", "fixed", "percent")
    search_fields = ("operation", "channel")