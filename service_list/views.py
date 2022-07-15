from django.shortcuts import get_object_or_404
from permissions.permissions import CreationPermissions, RUDOwnerPermissions
from pets.models import Pet
from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import (
    ListAPIView,
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)

from service_list.models import ServiceList
from service_list.serializers import ServiceListSerializer


class ListCreateServiceListView(ListCreateAPIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [CreationPermissions]

    queryset = ServiceList.objects.all()
    serializer_class = ServiceListSerializer
    lookup_url_kwarg = "pet_id"

    def perform_create(self, serializer):
        pet = get_object_or_404(Pet, pk=self.kwargs["pet_id"])

        serializer.save(pet=pet)

    def get_queryset(self):
        pet = get_object_or_404(Pet, pk=self.kwargs["pet_id"])

        if self.request.method == "GET":
            service_lists = ServiceList.objects.filter(pet_id__exact=pet)
            return service_lists
        return super().get_queryset()


class ListServiceList(ListAPIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [RUDOwnerPermissions]

    queryset = ServiceList.objects.all()
    serializer_class = ServiceListSerializer


class ServiceListDetailsView(RetrieveUpdateDestroyAPIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [RUDOwnerPermissions]

    queryset = ServiceList.objects.all()
    serializer_class = ServiceListSerializer
    lookup_url_kwarg = "service_list_id"
