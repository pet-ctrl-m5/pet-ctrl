from django.urls import path
from . import views

urlpatterns = [
    path("reports/", views.ListReportsView.as_view()),  # ver todos os laudos
    path(
        "reports/<int:report_id>/", views.ReportsDetailsView.as_view()
    ),  # ver todos os laudos
    path(
        "reports/pets/<int:pet_id>", views.CreateReportView.as_view()
    ),  # criar laudo ou ver todos os laudos de um pet
]
