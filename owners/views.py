from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView

from .utils import ListCreateOwnerMixin
from .serializers import CreateOwnerSerializer, ListOwnersSerializer
from .models import Owner


class ListCreateOwnerView(ListCreateOwnerMixin, ListCreateAPIView):

    queryset = Owner.objects.all()
    serializer_map = {"GET": ListOwnersSerializer, "POST": CreateOwnerSerializer}

    # def perform_create(self, serializer):
    #     user = self.request.user
    #     serializer.save(created_by=user)

class RetrieveUpdateOwnerView(RetrieveUpdateDestroyAPIView):
    lookup_url_kwarg = "owner_id"

    queryset = Owner.objects.all()
    serializer_class = CreateOwnerSerializer
