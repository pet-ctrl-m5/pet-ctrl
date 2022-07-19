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
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView, Response, status
from store.models import Store

from staffs.models import Staff
from staffs.serializers import ListStaffsSerializer, RegisterSerializer

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


class RetrieveStaffByToken(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        serialized = RegisterSerializer(instance=user)

        return Response(serialized.data, status.HTTP_200_OK)
