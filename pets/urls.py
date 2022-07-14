from django.urls import path

from . import views

urlpatterns = [
    path("pets/owner/<int:owner_id>/", views.ListCreatePetView.as_view()),
    path("pets/", views.ListPetsView.as_view()),
    path("pets/<int:pet_id>/", views.PetsDetailsView.as_view()),
]
