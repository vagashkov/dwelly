from django.urls import path, include

from .api import RegisterAccount

urlpatterns = [
    path("register", RegisterAccount.as_view(), name="rest_register"),
    path("", include("dj_rest_auth.urls")),
]
