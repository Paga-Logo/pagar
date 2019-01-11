import uuid

from django.db import models

# Create your models here.


class Debt(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nature_of_debt = models.CharField(max_length=200, blank=False, null=False)
    original_value = models.DecimalField(decimal_places=2, null=False, max_digits=10)
    current_value = models.DecimalField(decimal_places=2, null=False, max_digits=10)
    discount_percentage = models.FloatField(null=False)
