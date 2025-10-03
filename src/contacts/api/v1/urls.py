from django.urls import path, include

from .views import CreateCompany

urlpatterns = [
    path(
        "addresses/",
        include("contacts.api.v1.addresses.urls")
    ),
    path(
        "contacts/",
        include("contacts.api.v1.contacts.urls")
    ),
    path(
        "user_messages/",
        include("contacts.api.v1.user_messages.urls")
    ),
    path(
        "",
        CreateCompany.as_view(),
        name="api_company"
    )
]
