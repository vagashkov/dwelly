from django.urls import path

from .views import Contacts

app_name = "contacts"

urlpatterns = [
    path("", Contacts.as_view(), name="company_info"),
]
