from django.urls import path, include

urlpatterns = [
    # allauth urls
    path(
        "auth/",
        include("allauth.urls")
    ),
    # profile urls
    path(
        "profile/",
        include("users.profile.urls")
        ),
    # API urls
    path(
        "api/",
        include("users.api.urls"),
    ),
]
