from rest_framework import serializers

from .models import Pet


class PetCreationSerializer(serializers.ModelSerializer):
    owner_id = serializers.SerializerMethodField()

    class Meta:
        model = Pet
        fields = [
            "id",
            "name",
            "type",
            "breed",
            "birthday",
            "is_alive",
            "owner_id",
        ]
        extra_kwargs = {"owner": {"write_only": True}}

    def get_owner_id(self, obj: Pet) -> int:

        return obj.owner.id


class PetRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pet
        fields = "__all__"
        depth = 1
