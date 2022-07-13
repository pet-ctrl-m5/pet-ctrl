from permissions.permissions import CreationPermissions
from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)

from .mixins import ListCreateOwnerMixin
from .models import Owner
from .serializers import CreateOwnerSerializer, ListOwnersSerializer


class ListCreateOwnerView(ListCreateOwnerMixin, ListCreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [CreationPermissions]

    queryset = Owner.objects.all()
    serializer_map = {
        "GET": ListOwnersSerializer,
        "POST": CreateOwnerSerializer,
    }

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(created_by=user)


class RetrieveUpdateOwnerView(RetrieveUpdateDestroyAPIView):
    lookup_url_kwarg = "owner_id"

    queryset = Owner.objects.all()
    serializer_class = CreateOwnerSerializer
