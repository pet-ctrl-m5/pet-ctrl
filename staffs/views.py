from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView

from staffs.models import Staff
from staffs.serializers import RegisterSerializer

# Create your views here.


class ListCreateStaffView(ListCreateAPIView):
    queryset = Staff.objects.all()
    serializer_class = RegisterSerializer


class DetailStaffView(RetrieveUpdateDestroyAPIView):
    queryset = Staff.objects.all()
    serializer_class = RegisterSerializer
