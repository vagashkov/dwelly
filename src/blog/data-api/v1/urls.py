from django.urls import path, include

urlpatterns = [
   path(
      "tags/",
      include("blog.data-api.v1.tags.urls")
   ),
   path(
      "statuses/",
      include("blog.data-api.v1.statuses.urls")
   )
]
