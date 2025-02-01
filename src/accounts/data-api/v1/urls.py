from django.urls import path, include

from .views import Accounts

urlpatterns = [
    path("auth/", include("dj_rest_auth.urls")),
    path("register", Accounts.as_view(), name="rest_register"),
]
