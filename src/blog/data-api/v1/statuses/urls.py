from django.urls import path

from .views import Statuses, StatusDetails

urlpatterns = [
    path(
        "<str:name>",
        StatusDetails.as_view(),
        name="blog_api_status_details"
    ),
    path(
        "",
        Statuses.as_view(),
        name="blog_api_statuses"
    )
]
