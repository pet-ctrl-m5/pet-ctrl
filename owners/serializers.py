from pets.serializers import (
    OwnerPetRetrieveSerializer,
    PetCreationSerializer,
    PetRetrieveSerializer,
)
from rest_framework import serializers

from .models import Owner


class ListOwnersSerializer(serializers.ModelSerializer):

    pets = OwnerPetRetrieveSerializer(read_only=True, many=True)

    class Meta:
        model = Owner
        fields = [
            "id",
            "name",
            "email",
            "address",
            "phone_number",
            "created_by",
            "pets",
        ]


class CreateOwnerSerializer(serializers.ModelSerializer):
    pets = PetCreationSerializer(read_only=True, many=True)

    class Meta:
        model = Owner
        fields = [
            "id",
            "name",
            "email",
            "address",
            "phone_number",
            "created_by",
            "pets",
        ]
        extra_kwargs = {"created_by": {"read_only": True}}
