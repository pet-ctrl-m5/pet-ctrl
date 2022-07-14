from django.shortcuts import render
# Create your views here.
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView
from .models import Store
from .serializers import ListStoreSerializer, CreateStoreSerializer

class ListCreateStoreView(ListCreateAPIView):

    queryset = Store.objects.all()
    serializer_map = {
        "GET": ListStoreSerializer,
        "POST": CreateStoreSerializer,
    }

class RetrieveUpdateStoreView(RetrieveUpdateAPIView):

    queryset = Store.objects.all()
    serializer_class = CreateStoreSerializer
    