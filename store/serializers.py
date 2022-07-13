from rest_framework import serializers
from .models import Store


class ListStoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = "__all__"


class CreateStoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = "__all__"