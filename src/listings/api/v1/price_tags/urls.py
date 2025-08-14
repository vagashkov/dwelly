from django.urls import path

from .views import PriceTagsList

urlpatterns = [
    path(
        "",
        PriceTagsList.as_view(),
        name="api_listing_price_tags"
    ),
]
