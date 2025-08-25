from django.urls import path

from .views import Statuses, StatusDetails

urlpatterns = [
    path(
        "<str:name>",
        StatusDetails.as_view(),
        name="api_reservation_status_details"
    ),
    path(
        "",
        Statuses.as_view(),
        name="api_reservation_statuses"
    )
]
