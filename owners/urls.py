from django.urls import path

from .views import ListCreateOwnerView, RetrieveUpdateOwnerView

urlpatterns = [
    path("owners/", ListCreateOwnerView.as_view()),
    path("owners/<int:owner_id>/", RetrieveUpdateOwnerView.as_view())
]
