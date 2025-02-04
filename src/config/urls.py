"""
URL configuration for config project.

"""
from django.contrib import admin
from django.urls import path, include

from core.views import HomeView

urlpatterns = [
    path('admin/', admin.site.urls),

    # user accounts and profiles management
    path(
        "accounts/",
        include("accounts.urls")
    ),

    # OpenAPI-related views
    path(
        "api-schema/",
        include("config.api-schema.urls")
    ),

    # homepage
    path("", HomeView.as_view(), name="home")
]
