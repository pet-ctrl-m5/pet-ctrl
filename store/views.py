from urllib import request

from django.shortcuts import get_object_or_404
from rest_framework.authentication import TokenAuthentication

# Create your views here.
from rest_framework.generics import (
    ListAPIView,
    ListCreateAPIView,
    RetrieveUpdateAPIView,
)
from service_list.models import ServiceList
from service_list.serializers import FinancialReportSerializer

from permissions.permissions import (
    FinancialReportsPermission,
    StoreCRUDPermission,
)

from .models import Store
from .serializers import CreateStoreSerializer, ListStoreSerializer


class ListCreateStoreView(ListCreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [StoreCRUDPermission]

    queryset = Store.objects.filter(is_active__exact=True)

    serializer_class = CreateStoreSerializer


class RetrieveUpdateStoreView(RetrieveUpdateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [StoreCRUDPermission]

    queryset = Store.objects.all()
    serializer_class = ListStoreSerializer


class FinancialReports(ListAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [FinancialReportsPermission]

    queryset = ServiceList.objects.all()
    serializer_class = FinancialReportSerializer

    def get_queryset(self):

        route_parameter = self.request.GET.get("store")

        if route_parameter == "null":
            queryset = ServiceList.objects.filter(delivered_at__exact=None)
            return queryset

        get_object_or_404(Store, pk=route_parameter)

        queryset = ServiceList.objects.filter(
            delivered_at__exact=route_parameter
        )

        return queryset
