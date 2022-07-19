from django.shortcuts import get_object_or_404, render
from permissions.permissions import (
    StaffCreationPermission,
    StaffCRUDPermission,
)
from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    RetrieveUpdateDestroyAPIView,
)
from store.models import Store

from staffs.models import Staff
from staffs.serializers import RegisterSerializer

# Create your views here.


class CreateStaffView(CreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [StaffCreationPermission]

    queryset = Staff.objects.all()
    serializer_class = RegisterSerializer
    lookup_url_kwarg = "store_id"

    def perform_create(self, serializer):
        store = get_object_or_404(
            Store.objects.filter(is_active__exact=True),
            pk=self.kwargs["store_id"],
        )

        serializer.save(store=store)


class ListStaffView(ListAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [StaffCRUDPermission]

    queryset = Staff.objects.all()
    serializer_class = RegisterSerializer


class DetailStaffView(RetrieveUpdateDestroyAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [StaffCRUDPermission]

    queryset = Staff.objects.all()
    serializer_class = RegisterSerializer
