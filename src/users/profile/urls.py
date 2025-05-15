from django.urls import path

from .views import DisplayProfile, EditProfile

urlpatterns = [
    path(
        "",
        DisplayProfile.as_view(),
        name="user_display_profile"
    ),
    path(
        "edit",
        EditProfile.as_view(),
        name="user_edit_profile"
    ),
]
