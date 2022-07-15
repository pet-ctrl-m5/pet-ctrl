from django.shortcuts import render
from permissions.permissions import ServicesCRUDPermission
from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView

from .models import Service
from .serializers import ServiceSerializer


class ListCreateServiceView(ListCreateAPIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [ServicesCRUDPermission]

    # queryset = Service.objects.all()
    queryset = Service.objects.filter(is_active__exact=True)
    serializer_class = ServiceSerializer


class ServiceDetailsView(RetrieveUpdateAPIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [ServicesCRUDPermission]

    queryset = Service.objects.filter(is_active__exact=True)
    serializer_class = ServiceSerializer
    lookup_url_kwarg = "service_id"
