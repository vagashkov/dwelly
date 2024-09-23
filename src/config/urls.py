"""
URL configuration for config project.
"""

from django.contrib import admin
from django.urls import path, include

from .views import HomeView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("allauth.urls")),
    path("", HomeView.as_view(), name="home")
]
