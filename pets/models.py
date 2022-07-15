from django.db import models


class Pet(models.Model):
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=30)
    breed = models.CharField(max_length=30)
    birthday = models.DateField()
    is_alive = models.BooleanField(default=True)
    owner = models.ForeignKey(
        "owners.Owner",
        on_delete=models.SET_NULL,
        related_name="pets",
        null=True,
    )
