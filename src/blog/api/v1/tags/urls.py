from django.urls import path

from .views import Tags, TagDetails

urlpatterns = [
    path(
        "<str:name>",
        TagDetails.as_view(),
        name="api_tag_details"
    ),
    path(
        "",
        Tags.as_view(),
        name="api_tags"
    )
]
