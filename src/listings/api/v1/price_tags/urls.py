from django.urls import path

from .views import PriceTagsList, DayRatesList

urlpatterns = [
    path(
        "price_tags/",
        PriceTagsList.as_view(),
        name="api_listing_price_tags"
    ),

    path(
        "daily_rates/",
        DayRatesList.as_view(),
        name="api_listing_daily_rates"
    ),
]
