from django.urls import path

from .views import PhotosList

urlpatterns = [
    path(
        "",
        PhotosList.as_view(),
        name="api_listing_photos"
    ),
]
