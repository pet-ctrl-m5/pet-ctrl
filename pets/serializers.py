from reports.serializers import ReportListPetSerializer, ReportSerializer
from rest_framework import serializers
from service_list.serializers import ServiceListSerializer

from .models import Pet


#
class PetCreationSerializer(serializers.ModelSerializer):
    owner_id = serializers.SerializerMethodField()
    reports = ReportSerializer(read_only=True, many=True)

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
            "reports",
        ]
        extra_kwargs = {"owner": {"write_only": True}}

    def get_owner_id(self, obj: Pet) -> int:

        return obj.owner.id


class PetRetrieveSerializer(serializers.ModelSerializer):
    owner_info = serializers.SerializerMethodField()
    reports = ReportListPetSerializer(read_only=True, many=True)
    customer_services = ServiceListSerializer(read_only=True, many=True)

    class Meta:
        model = Pet
        fields = [
            "id",
            "name",
            "type",
            "breed",
            "birthday",
            "is_alive",
            "owner_info",
            "reports",
            "customer_services",
        ]
        extra_kwargs = {"owner": {"write_only": True}}
        depth = 0

    def get_owner_info(self, obj: Pet) -> dict:
        info = {
            "id": obj.owner.id,
            "name": obj.owner.name,
            "phone_number": obj.owner.phone_number,
            "email": obj.owner.email,
        }
        return info


class OwnerPetRetrieveSerializer(serializers.ModelSerializer):

    reports = ReportSerializer(read_only=True, many=True)

    class Meta:
        model = Pet
        fields = [
            "id",
            "name",
            "type",
            "breed",
            "birthday",
            "is_alive",
            "reports",
        ]
        extra_kwargs = {"owner": {"write_only": True}}
        # depth = 1
