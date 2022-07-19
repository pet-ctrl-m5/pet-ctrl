from django.db import models


class Report(models.Model):
    report = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    pet = models.ForeignKey(
        "pets.Pet",
        on_delete=models.SET_NULL,
        related_name="reports",
        null=True,
    )
