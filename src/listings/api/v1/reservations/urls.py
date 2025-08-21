from django.urls import path

from .views import ListingReservations

urlpatterns = [
    path(
        "",
        ListingReservations.as_view(),
        name="api_listing_reservations"
    ),
]
