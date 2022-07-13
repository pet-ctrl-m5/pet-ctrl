from rest_framework import serializers

from .models import ServiceList


class ServiceListSerializer(serializers.ModelSerializer):
    total = serializers.SerializerMethodField()
    pet_id = serializers.SerializerMethodField()

    class Meta:
        model = ServiceList
        fields = "__all__"
        extra_kwargs = {"pet": {"write_only": True}}

    def get_total(self, obj: ServiceList) -> float:
        total_value = sum(item["price"] for item in obj.pet_services)
        return total_value - total_value * obj.discount

    def get_pet_id(self, obj: ServiceList) -> int:
        return obj.pet.id
