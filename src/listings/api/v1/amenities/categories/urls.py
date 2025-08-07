from django.urls import path

from .views import Categories, CategoryDetails

urlpatterns = [
    path(
        "<str:name>",
        CategoryDetails.as_view(),
        name="api_category_details"
    ),
    path(
        "",
        Categories.as_view(),
        name="api_categories"
    )
]
