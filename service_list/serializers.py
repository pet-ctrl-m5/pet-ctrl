from rest_framework import serializers
from services.models import Service
from services.serializers import ServiceSerializer, ServicesToListSerializer

from service_list.exceptions import ServiceDoesNotExists

from .models import ServiceList


class ServiceListSerializer(serializers.ModelSerializer):

    pet_id = serializers.SerializerMethodField()
    pet_services = ServicesToListSerializer(many=True)

    class Meta:
        model = ServiceList
        # fields = "__all__"
        exclude = ["pet"]
        extra_kwargs = {
            # "pet": {"write_only": True},
            "total": {"read_only": True},
            "delivered_at": {"read_only": True},
        }

    def validate_discount(self, value):
        if value < 0 or value > 100:
            raise serializers.ValidationError(
                "Ensure discount is a number between 0 and 100"
            )
        return value

    def get_pet_id(self, obj: ServiceList) -> int:
        if obj.pet is not None:
            return obj.pet.id
        return None

    def create(self, validated_data: dict) -> ServiceList:
        services_list = validated_data.pop("pet_services", None)
        discount = validated_data.pop("discount", 0)

        list_to_add = []

        for item in services_list:
            service = Service.objects.filter(
                name__iexact=item["name"], is_active__exact=True
            ).first()

            if not service:
                raise ServiceDoesNotExists

            list_to_add.append(service)

        sub_total = sum(item.price for item in list_to_add)

        total_value = sub_total - (sub_total * discount) / 100

        new_sl = ServiceList.objects.create(
            **validated_data, total=total_value, discount=discount
        )
        new_sl.pet_services.set(list_to_add)

        return new_sl

    def update(
        self, instance: ServiceList, validated_data: dict
    ) -> ServiceList:

        services_list = validated_data.pop("pet_services", None)
        discount = validated_data.pop("discount", None)

        if discount is not None:
            # instance.discount = discount
            setattr(instance, "discount", discount)

        list_to_add = []

        if services_list:
            for item in services_list:
                service = Service.objects.filter(
                    name__iexact=item["name"], is_active__exact=True
                ).first()

                if not service:
                    raise ServiceDoesNotExists

                list_to_add.append(service)

        sub_total = sum(item.price for item in list_to_add)

        total_value = sub_total - (sub_total * discount) / 100

        instance.total = total_value
        instance.pet_services.set(list_to_add)

        instance.save()

        return instance


class FinancialReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceList
        fields = ["id", "pet_id", "created_at", "discount", "total"]
