from django.urls import path
from rest_framework.authtoken import views

from . import views as s_views

urlpatterns = [
    path("staffs/register/", s_views.ListCreateStaffView.as_view()),
    path("staffs/<pk>/", s_views.DetailStaffView.as_view()),
    path("login/", views.obtain_auth_token),
]
