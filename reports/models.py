from django.db import models


class Report(models.Model):
    report = models.TextField()
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField()
    pet = models.ForeignKey(
        "pets.Pet", on_delete=models.CASCADE, related_name="reports"
    )
