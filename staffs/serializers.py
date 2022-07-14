from rest_framework import serializers

from .models import Staff


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Staff
        fields = [
            "id",
            "username",
            "first_name",
            "last_name",
            "is_active",
            "is_superuser",
            "is_manager",
            "is_doctor",
            "is_staff",
            "date_joined",
            "password",
            "store",
        ]
        extra_kwargs = {
            "password": {"write_only": True},
            "date_joined": {"read_only": True},
        }

    def create(self, validated_data):
        return Staff.objects.create_user(**validated_data)


class ListStaffsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Staff
        fields = ["id", "username", "first_name", "last_name", "is_active"]

    def create(self, validated_data):
        return Staff.objects.create_user(**validated_data)
