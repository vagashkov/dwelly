from django.urls import path, include

urlpatterns = [
    path(
        "object_types/",
        include("listings.api.v1.object_types.urls")
    ),
    path(
        "amenities/",
        include("listings.api.v1.amenities.urls")
    ),
    path(
        "house_rules/",
        include("listings.api.v1.house_rules.urls")
    ),
]
