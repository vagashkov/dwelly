from django.urls import path, include

from .views import Contacts

app_name = "contacts"

urlpatterns = [
    # API urls
    path("api/", include("contacts.api.urls")),
    # Contacts page
    path("", Contacts.as_view(), name="company_info"),
]
