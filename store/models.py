from django.db import models

class Store(models.Model):

    name = models.CharField(max_length=255, unique=True)
    adress = models.CharField(max_length=255)
    city = models.CharField(max_length=50)
    state = models.TextChoices()
    is_active = models.BooleanField(default=True)
    staff = models.CharField()
