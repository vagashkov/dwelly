from django.urls import path, include

urlpatterns = [
    # allauth urls
    path(
        "auth/",
        include("allauth.urls")
    ),
    # API urls
    path(
        "api/",
        include("accounts.data-api.urls"),
    ),
]
