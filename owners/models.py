from django.db import models


class Owner(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    address = models.TextField()
    phone_number = models.CharField(max_length=20)
    created_by = models.ForeignKey(
        "staffs.Staff",
        on_delete=models.SET_NULL,
        related_name="customers",
        null=True,
    )
