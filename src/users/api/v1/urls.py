from django.urls import path, include

from .views import (
    Users, Profiles,
    DisplayProfile, UserProfile
)

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
    # user profile
    path(
        "profile",
        UserProfile.as_view(),
        name="rest_user_profile"
    ),
    # profiles section (for admins only)
    path(
        "profiles",
        Profiles.as_view(),
        name="rest_profiles"
    ),
    path(
        "profiles/<str:public_id>",
        DisplayProfile.as_view(),
        name="rest_profile_details"
    ),
]
