from rest_framework import serializers

from .models import Report


class ReportSerializer(serializers.ModelSerializer):

    pet_info = serializers.SerializerMethodField()

    class Meta:
        model = Report
        fields = ["id", "report", "created_at", "updated_at", "pet_info"]
        # exclude = ["pet"]
        extra_kwargs = {"pet": {"write_only": True}}

    def get_pet_info(self, obj: Report) -> dict:
        return {
            "id": obj.pet.id,
            "name": obj.pet.name,
            "owner": obj.pet.owner.name,
        }
