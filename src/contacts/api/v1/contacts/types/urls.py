from django.urls import path

from .views import ContactTypes, ContactTypeDetails

urlpatterns = [
    path(
        "<str:name>",
        ContactTypeDetails.as_view(),
        name="api_company_contact_type_details"
    ),
    path(
        "",
        ContactTypes.as_view(),
        name="api_company_contact_types"
    )
]
