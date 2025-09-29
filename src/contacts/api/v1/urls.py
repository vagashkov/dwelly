from django.urls import path, include

from .views import CreateCompany

urlpatterns = [
    path(
        "addresses/",
        include("contacts.api.v1.addresses.urls")
    ),
    path(
        "",
        CreateCompany.as_view(),
        name="api_company"
    )
]
