from rest_framework import serializers

from .models import Report

from pets.serializers import PetRetrieveSerializer


class ReportSerializer(serializers.ModelSerializer):
    pet_id = PetRetrieveSerializer(read_only=True)

    pet_info = serializers.SerializerMethodField()

    class Meta:
        model = Report
        fields = "__all__"
        read_only_fields = ["id", "created_at", "updated_at"]

    def get_pet_info(self, obj: Report) -> dict:
        return {"name": obj.pet.name, "owner": obj.pet.owner.first_name}
