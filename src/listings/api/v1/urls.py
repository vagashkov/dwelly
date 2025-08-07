from django.urls import path, include

urlpatterns = [
    path(
        "object_types/",
        include("listings.api.v1.object_types.urls")
    ),
]
