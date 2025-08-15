from django.urls import path, include

urlpatterns = [
    path(
        "v1/",
        include("listings.api.v1.urls")
    )
]
