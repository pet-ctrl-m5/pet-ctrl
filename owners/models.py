from django.db import models


class Owner(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    address = models.TextField()
    phone_number = models.IntegerField()
    created_by = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, related_name="customers", null=True
    )
