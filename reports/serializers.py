from rest_framework import serializers

from .models import Report


class ReportSerializer(serializers.ModelSerializer):

    pet_info = serializers.SerializerMethodField()

    class Meta:
        model = Report
        fields = ["id", "report", "created_at", "updated_at", "pet_info"]
        # exclude = ["pet"]
        extra_kwargs = {"pet": {"write_only": True}}

    def get_pet_info(self, obj: Report) -> dict | None:

        if obj.pet is not None:
            owner = obj.pet.owner
            if owner is not None:
                owner_name = obj.pet.owner.name
            else:
                owner_name = None
                return {
                    "id": obj.pet.id,
                    "name": obj.pet.name,
                    "owner": owner_name,
                }

        return None


class ReportListPetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = ["id", "report", "created_at", "updated_at"]
        # exclude = ["pet"]
        extra_kwargs = {"pet": {"write_only": True}}
