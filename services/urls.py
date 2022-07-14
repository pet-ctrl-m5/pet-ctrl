from django.urls import path

from . import views

urlpatterns = [
    path("services/", views.ListCreateServiceView.as_view()),
    path("services/<int:service_id>", views.ServiceDetailsView.as_view()),
]
