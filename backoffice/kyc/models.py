import uuid

from django.db import models

class KYCCase(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("verified", "Verified"),
        ("rejected", "Rejected"),
    ]
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    customer_id = models.UUIDField()
    document_no = models.CharField(max_length=64)
    status = models.CharField(max_length=16, choices=STATUS_CHOICES, default="pending")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"KYC {self.document_no} ({self.status})"