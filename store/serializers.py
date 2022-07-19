from rest_framework import serializers
from service_list.serializers import FinancialReportSerializer
from staffs.serializers import ListStaffsSerializer

from .models import Store


class ListStoreSerializer(serializers.ModelSerializer):
    staffs = ListStaffsSerializer(read_only=True, many=True)

    class Meta:
        model = Store
        fields = [
            "id",
            "name",
            "address",
            "city",
            "state",
            "is_active",
            "staffs",
        ]

    # def validate_name(self, value):

    #     qs = Store.objects.filter(name__iexact=value, is_active__exact=True)

    #     if self.context["request"].method == "POST" and len(qs) > 0:
    #         raise serializers.ValidationError("Store already exists.")

    #     return value

    def update(self, instance: Store, validated_data):
        activity = validated_data.pop("is_active", None)

        if activity is not None and activity is not True:
            instance.is_active = False
            instance.save()

            return instance

        for key, value in validated_data.items():
            setattr(instance, key, value)

        instance.save()

        return instance


class CreateStoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = "__all__"

    def validate_name(self, value):

        qs = Store.objects.filter(name__iexact=value, is_active__exact=True)

        if self.context["request"].method == "POST" and len(qs) > 0:
            raise serializers.ValidationError("Store already exists.")

        return value
