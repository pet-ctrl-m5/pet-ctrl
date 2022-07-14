from django.shortcuts import get_object_or_404, render
from owners.models import Owner
from rest_framework.generics import ListAPIView, ListCreateAPIView

from pets.models import Pet
from pets.serializers import (
    PetCreationSerializer,
    PetRetrieveSerializer,
    RetrieveUpdateDestroyAPIView,
)

from .mixins import ListCreatePetMixin


class ListCreatePetView(ListCreatePetMixin, ListCreateAPIView):

    queryset = Pet.objects.all()
    # serializer_class = PetCreationSerializer
    serializer_map = {
        "GET": PetRetrieveSerializer,
        "POST": PetCreationSerializer,
    }

    lookup_url_kwarg = "owner_id"

    def perform_create(self, serializer):
        owner = get_object_or_404(Owner, pk=self.kwargs["owner_id"])

        serializer.save(owner=owner)

    def get_queryset(self):
        owner_id = get_object_or_404(Owner, pk=self.kwargs["owner_id"])

        if self.request.method == "GET":
            pets = Pet.objects.filter(owner_id__exact=owner_id)
            return pets
        return super().get_queryset()


class ListPetsView(ListAPIView):

    queryset = Pet.objects.all()
    serializer_class = PetRetrieveSerializer


class PetsDetailsView(RetrieveUpdateDestroyAPIView):
    queryset = Pet.objects.all()
    serializer_class = PetRetrieveSerializer
    lookup_url_kwarg = "pet_id"
