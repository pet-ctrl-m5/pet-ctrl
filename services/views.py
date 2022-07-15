from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView

from .models import Service
from .serializers import ServiceSerializer


class ListCreateServiceView(ListCreateAPIView):
    # queryset = Service.objects.all()
    queryset = Service.objects.filter(is_active__exact=True)
    serializer_class = ServiceSerializer


class ServiceDetailsView(RetrieveUpdateAPIView):
    queryset = Service.objects.filter(is_active__exact=True)
    serializer_class = ServiceSerializer
    lookup_url_kwarg = "service_id"
