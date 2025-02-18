"""
URL configuration for config project.

"""
from django.conf import settings
from django.conf.urls.static import static
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

    # blog application urls
    path(
        "blog/",
        include("blog.urls")
    ),

    # OpenAPI-related views
    path(
        "api-schema/",
        include("config.api-schema.urls")
    ),

    # homepage
    path("", HomeView.as_view(), name="home")
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )

    from debug_toolbar.toolbar import debug_toolbar_urls
    urlpatterns += debug_toolbar_urls()
