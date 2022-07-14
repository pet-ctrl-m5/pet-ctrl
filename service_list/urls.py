from django.urls import path

from . import views

urlpatterns = [
    path(
        "pets/<int:pet_id>/servicelist/",
        views.ListCreateServiceListView.as_view(),
    ),
    path("servicelist/", views.ListServiceList.as_view()),
    path(
        "servicelist/<int:service_list_id>/",
        views.ServiceListDetailsView.as_view(),
    ),
]
