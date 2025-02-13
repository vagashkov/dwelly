from django.urls import path

from .views import Posts, PostDetails

urlpatterns = [
    path(
        "<slug:slug>",
        PostDetails.as_view(),
        name="blog_api_post_details"
    ),
    path(
        "",
        Posts.as_view(),
        name="blog_api_posts"
    )
]
