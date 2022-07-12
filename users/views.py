from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView

from users.models import User
from users.serializers import RegisterSerializer

# Create your views here.


class ListCreateUserView(ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
