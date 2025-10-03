from django.urls import path, include

from .views import CompanyContacts, ContactDetails

urlpatterns = [
    path(
        "contact_types/",
        include("contacts.api.v1.contacts.types.urls")
    ),
    path(
        "<int:id>",
        ContactDetails.as_view(),
        name="api_company_contact_details"
    ),
    path(
        "",
        CompanyContacts.as_view(),
        name="api_company_contacts"
    )
]
