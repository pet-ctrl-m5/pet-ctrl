from django.shortcuts import render
from rest_framework.authentication import TokenAuthentication

# Create your views here.
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView

from permissions.permissions import StoreCRUDPermission
from store.mixins import SerializeByMethodMixin

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
