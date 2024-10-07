from django.urls import path, include

urlpatterns = [
    # API urls
    path(
        "api/",
        include("accounts.api.urls"),
    ),
    # allauth urls
    path(
        "",
        include("allauth.urls")
    ),
]
