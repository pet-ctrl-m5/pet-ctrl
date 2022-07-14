from django.shortcuts import get_object_or_404, render
from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    RetrieveUpdateDestroyAPIView,
)
from store.models import Store

from staffs.models import Staff
from staffs.serializers import ListStaffsSerializer, RegisterSerializer

# Create your views here.


class CreateStaffView(CreateAPIView):
    queryset = Staff.objects.all()
    serializer_class = RegisterSerializer
    lookup_url_kwarg = "store_id"

    def perform_create(self, serializer):
        store = get_object_or_404(Store, pk=self.kwargs["store_id"])

        serializer.save(store=store)


class ListStaffView(ListAPIView):
    queryset = Staff.objects.all()
    serializer_class = RegisterSerializer


class DetailStaffView(RetrieveUpdateDestroyAPIView):
    queryset = Staff.objects.all()
    serializer_class = RegisterSerializer
