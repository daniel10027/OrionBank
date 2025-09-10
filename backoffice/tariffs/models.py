import uuid

from django.db import models

class Tariff(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    operation = models.CharField(max_length=32)
    channel = models.CharField(max_length=16)
    fixed = models.DecimalField(max_digits=18, decimal_places=2, default=0)
    percent = models.DecimalField(max_digits=5, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.operation}-{self.channel}"