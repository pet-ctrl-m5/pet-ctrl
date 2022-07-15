from django.shortcuts import get_object_or_404, render
from permissions.permissions import ReportsCRUDPermission
from pets.models import Pet
from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import (
    ListAPIView,
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)

from .models import Report
from .serializers import ReportSerializer


class ListCreateReportView(ListCreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [ReportsCRUDPermission]

    queryset = Report.objects.all()
    serializer_class = ReportSerializer
    lookup_url_kwarg = "pet_id"

    def perform_create(self, serializer):

        pet = get_object_or_404(Pet, pk=self.kwargs["pet_id"])
        serializer.save(pet=pet)

    def get_queryset(self):
        pet = get_object_or_404(Pet, pk=self.kwargs["pet_id"])

        if self.request.method == "GET":
            reports = Report.objects.filter(pet_id__exact=pet)
            return reports
        return super().get_queryset()


class ListReportsView(ListAPIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [ReportsCRUDPermission]

    queryset = Report.objects.all()
    serializer_class = ReportSerializer


class ReportsDetailsView(RetrieveUpdateDestroyAPIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [ReportsCRUDPermission]

    queryset = Report.objects.all()
    serializer_class = ReportSerializer
    lookup_url_kwarg = "report_id"
