from rest_framework import serializers
from .models import Owner


class ListOwnersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Owner
        fields = "__all__"


class CreateOwnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Owner
        fields = "__all__"
        # extra_kwargs = {"created_by": {"read_only": True}}
