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
            "is_superuser",
            "is_active",
            "is_manager",
            "is_doctor",
            "date_joined",
            "password",
        ]
        extra_kwargs = {
            "password": {"write_only": True},
            "date_joined": {"read_only": True},
        }

    def create(self, validated_data):
        return Staff.objects.create_user(**validated_data)


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
