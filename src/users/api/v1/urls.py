from django.urls import path, include

from .views import Users, Profiles, ProfileDetails

urlpatterns = [
    # user authentication section
    path(
        "auth/",
        include("dj_rest_auth.urls")
    ),
    # user registration endpoint
    path(
        "register",
        Users.as_view(),
        name="rest_register"
    ),
    # profiles section (for admins only)
    path(
        "profiles",
        Profiles.as_view(),
        name="rest_profiles"
    ),
    path(
        "profiles/<int:id>",
        ProfileDetails.as_view(),
        name="rest_profile_details"
    ),
]
