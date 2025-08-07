from django.urls import path

from .views import ObjectTypes, ObjectTypeDetails

urlpatterns = [
    path(
        "<str:name>",
        ObjectTypeDetails.as_view(),
        name="api_object_type_details"
    ),
    path(
        "",
        ObjectTypes.as_view(),
        name="api_object_types"
    )
]
