from django.urls import path, include

from .api import Accounts, Details

urlpatterns = [
    path("auth", include("dj_rest_auth.urls")),
    path("<id>", Details.as_view(), name="rest_account_details"),
    path("", Accounts.as_view(), name="rest_accounts"),
]
