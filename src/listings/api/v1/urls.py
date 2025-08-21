from django.urls import path, include

from .views import Listings, ListingDetails

urlpatterns = [
    # Object types module
    path(
        "object_types/",
        include("listings.api.v1.object_types.urls")
    ),
    # Amenities and categories module
    path(
        "amenities/",
        include("listings.api.v1.amenities.urls")
    ),
    # House rules module
    path(
        "house_rules/",
        include("listings.api.v1.house_rules.urls")
    ),
    # Single listing details
    path(
        "<slug:slug>",
        ListingDetails.as_view(),
        name="api_listing_details"
    ),
    path(
        "<slug:slug>/photos/",
        include(
            "listings.api.v1.photos.urls"
        )
    ),
    path(
        "<slug:slug>/rates/",
        include(
            "listings.api.v1.price_tags.urls"
        )
    ),
    path(
        "<slug:slug>/reservations/",
        include(
            "listings.api.v1.reservations.urls"
        )
    ),
    # Listing list
    path(
        "",
        Listings.as_view(),
        name="api_list"
    )
]
