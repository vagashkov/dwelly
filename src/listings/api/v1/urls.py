from django.urls import path, include

urlpatterns = [
    path(
        "amenities/",
        include("listings.api.v1.amenities.urls")
    ),
    path(
        "object_types/",
        include("listings.api.v1.object_types.urls")
    ),
]
