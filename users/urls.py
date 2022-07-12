from django.urls import path

from . import views

urlpatterns = [path("users/register/", views.ListCreateUserView.as_view())]
