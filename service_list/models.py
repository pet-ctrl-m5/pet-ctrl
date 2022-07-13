from django.db import models


class ServiceList(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    discount = models.FloatField()
    total = models.DecimalField(max_digits=5, decimal_places=2)
    pet = models.ForeignKey(
        "pets.Pet",
        on_delete=models.DO_NOTHING,
        related_name="customer_services",
    )
    pet_services = models.ManyToManyField("services.Service", related_name="services_list")
