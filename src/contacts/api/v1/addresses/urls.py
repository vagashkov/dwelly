from django.urls import path

from .views import CreateAddress

urlpatterns = [
    path(
        "",
        CreateAddress.as_view(),
        name="api_company_addresses"
    )
]
