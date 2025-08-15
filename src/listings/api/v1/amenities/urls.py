from django.urls import path, include

from .views import Amenities, AmenityDetails

urlpatterns = [
    path(
        "categories/",
        include("listings.api.v1.amenities.categories.urls")
    ),
    path(
        "<str:name>",
        AmenityDetails.as_view(),
        name="api_amenity_details"
    ),
    path(
        "",
        Amenities.as_view(),
        name="api_amenities"
    )
]
