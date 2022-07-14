from django.urls import path

from .views import ListCreateStoreView, RetrieveUpdateStoreView

urlpatterns = [
    path("stores/", ListCreateStoreView.as_view()),
    path("stores/<pk>/", RetrieveUpdateStoreView.as_view()),
]
