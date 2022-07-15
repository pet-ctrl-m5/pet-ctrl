from django.db import models


class ServiceList(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    discount = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    pet = models.ForeignKey(
        "pets.Pet",
        on_delete=models.SET_NULL,
        related_name="customer_services",
        null=True,
    )
    pet_services = models.ManyToManyField(
        "services.Service", related_name="services_list"
    )
