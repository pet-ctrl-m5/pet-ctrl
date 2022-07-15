from django.urls import path

from . import views

urlpatterns = [
    path(
        "pets/<int:pet_id>/serviceslist/",
        views.ListCreateServiceListView.as_view(),
    ),
    path("serviceslist/", views.ListServiceList.as_view()),
    path(
        "serviceslist/<int:service_list_id>/",
        views.ServiceListDetailsView.as_view(),
    ),
]
