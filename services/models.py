from django.db import models


class Service(models.Model):
    name = models.CharField(max_length=50)
    category = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
