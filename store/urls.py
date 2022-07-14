from django.urls import path
from .views import ListCreateStoreView, RetrieveUpdateStoreView
urlpatterns = [
    path("store/", ListCreateStoreView.as_view()),
    path("store/<pk>/", RetrieveUpdateStoreView.as_view())
]