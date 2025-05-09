from django.urls import path, include

from .views import Users

urlpatterns = [
    path("auth/", include("dj_rest_auth.urls")),
    path("register", Users.as_view(), name="rest_register"),
]
