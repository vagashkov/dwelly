from django.urls import path, include

urlpatterns = [
   path(
      "tags/",
      include("blog.api.v1.tags.urls")
   ),
   path(
      "statuses/",
      include("blog.api.v1.statuses.urls")
   ),
   path(
      "posts/",
      include("blog.api.v1.posts.urls")
   )
]
