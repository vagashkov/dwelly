from django.urls import path

from .views import Tags

urlpatterns = [
    path("", Tags.as_view(), name="blog_api_tags")
]
