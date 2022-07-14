from django.shortcuts import render
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)

from .models import Service
from .serializers import ServiceSerializer


class ListCreateServiceView(ListCreateAPIView):
    # queryset = Service.objects.all()
    queryset = Service.objects.filter(is_active__exact=True)
    serializer_class = ServiceSerializer


class ServiceDetailsView(RetrieveUpdateDestroyAPIView):
    queryset = Service.objects.filter(is_active__exact=True)
    serializer_class = ServiceSerializer
    lookup_url_kwarg = "service_id"
