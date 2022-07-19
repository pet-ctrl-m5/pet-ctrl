from django.urls import path
from rest_framework.authtoken import views

from . import views as s_views

urlpatterns = [
    path(
        "stores/<int:store_id>/staffs/register/",
        s_views.CreateStaffView.as_view(),
    ),
    path("staffs/", s_views.ListStaffView.as_view()),
    path("staffs/<pk>/", s_views.DetailStaffView.as_view()),
    path("login/", views.obtain_auth_token),
    path("staffs/me/data/", s_views.RetrieveStaffByToken.as_view()),
]
