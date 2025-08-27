from django.urls import path, include

from .views import (
    List, Details,
    SubmitReservation, ApproveReservation, CancelReservation
)

app_name = "listings"

urlpatterns = [
    # API urls
    path("api/", include("listings.api.urls")),

    path(
        "reservations/<str:public_id>/submit",
        SubmitReservation.as_view(),
        name="submit_reservation"
    ),
    path(
        "reservations/<str:public_id>/approve",
        ApproveReservation.as_view(),
        name="approve_reservation"
    ),
    path(
        "reservations/<str:public_id>/cancel",
        CancelReservation.as_view(),
        name="cancel_reservation"
    ),
    path("<slug:slug>", Details.as_view(), name="listing_details"),
    path("", List.as_view(), name="list"),
]
