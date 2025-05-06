"""
URL configuration for PetHotel project.

"""
from django.contrib import admin
from django.urls import path, include

from core.views import HomeView

urlpatterns = [
    path("admin/", admin.site.urls),

    # user accounts and profiles management
    path(
        "users/",
        include("users.urls")
    ),

    # homepage
    path("", HomeView.as_view(), name="home")
]
