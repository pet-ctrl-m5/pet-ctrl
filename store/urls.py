from django.urls import path
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView,
)

from .views import (
    FinancialReports,
    ListCreateStoreView,
    RetrieveUpdateStoreView,
)

urlpatterns = [
    path("stores/", ListCreateStoreView.as_view()),
    path("stores/financial/", FinancialReports.as_view()),
    path("stores/<pk>/", RetrieveUpdateStoreView.as_view()),
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "schema/swagger-ui/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path(
        "schema/redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"
    ),
]
