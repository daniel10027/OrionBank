from django.urls import path
from .views import transactions_report

urlpatterns = [
    path("transactions/", transactions_report),
]