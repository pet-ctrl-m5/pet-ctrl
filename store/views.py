from django.shortcuts import render

# Create your views here.
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView

from store.mixins import SerializeByMethodMixin

from .models import Store
from .serializers import CreateStoreSerializer, ListStoreSerializer


class ListCreateStoreView(ListCreateAPIView):

    queryset = Store.objects.filter(is_active__exact=True)

    serializer_class = CreateStoreSerializer


class RetrieveUpdateStoreView(RetrieveUpdateAPIView):

    queryset = Store.objects.all()
    serializer_class = ListStoreSerializer
