from rest_framework import serializers

from .models import Service


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = "__all__"
        read_only_fields = ["id", "created_at", "updated_at"]

    def validate_name(self, value):

        qs = Service.objects.filter(name__iexact=value, is_active__exact=True)

        if self.context["request"].method == "POST" and len(qs) > 0:
            raise serializers.ValidationError("Service already exists.")

        return value

    def update(self, instance: Service, validated_data):
        price = validated_data.pop("price", None)

        if price is not None and price != instance.price:
            new_service = Service.objects.create(
                name=instance.name,
                category=instance.category,
                price=price,
            )

            instance.is_active = False

            instance.save()

            for key, value in validated_data.items():
                setattr(new_service, key, value)

            new_service.save()

            return new_service

        for key, value in validated_data.items():
            setattr(instance, key, value)

        instance.save()

        return instance


class ServicesToListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ["id", "name", "category", "price"]
        extra_kwargs = {
            "category": {"read_only": True},
            "price": {"read_only": True},
        }
