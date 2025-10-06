from django.urls import path

from .views import (
    ListingReservations, ReservationDetails, ReservationVoucher
)

urlpatterns = [
    path(
        "<str:public_id>/voucher",
        ReservationVoucher.as_view(),
        name="api_reservation_voucher"
    ),
    path(
        "<str:public_id>",
        ReservationDetails.as_view(),
        name="api_reservation_details"
    ),
    path(
        "",
        ListingReservations.as_view(),
        name="api_listing_reservations"
    ),
]
