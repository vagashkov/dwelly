from django.urls import path, include

app_name = "listings"

urlpatterns = [
    # API urls
    path("api/", include("listings.api.urls")),
]
