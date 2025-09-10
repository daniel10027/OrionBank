from django.db import models
import uuid

class Dispute(models.Model):
    STATUS_CHOICES = [("open", "Open"), ("resolved", "Resolved")]
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    transaction_id = models.UUIDField()
    reason = models.TextField()
    status = models.CharField(max_length=16, choices=STATUS_CHOICES, default="open")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Dispute {self.transaction_id} ({self.status})"