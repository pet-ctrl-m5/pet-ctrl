from datetime import datetime, timedelta, timezone

from django.shortcuts import get_object_or_404
from django.utils import timezone
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
    pagination_class = None

    def get_queryset(self):

        store_id = self.request.GET.get("store")
        start = self.request.GET.get("start")
        finish = self.request.GET.get("finish")

        if not finish:
            finish = timezone.now().isoformat()
            # finish = finish.isoformat()

        if not start:
            conv_finish = datetime.fromisoformat(finish)
            start = conv_finish - timedelta(days=30)
            start = start.isoformat()

        if store_id == "null":
            queryset = ServiceList.objects.filter(
                delivered_at__exact=None, created_at__range=[start, finish]
            )
            return queryset

        get_object_or_404(Store, pk=store_id)

        queryset = ServiceList.objects.filter(
            delivered_at__exact=store_id, created_at__range=[start, finish]
        )

        return queryset
