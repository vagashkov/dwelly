from django.urls import path, include

from .views import List, Details

app_name = "listings"

urlpatterns = [
    # API urls
    path("api/", include("listings.api.urls")),

    path("", List.as_view(), name="list"),
    path("<slug:slug>", Details.as_view(), name="listing_details")
]
