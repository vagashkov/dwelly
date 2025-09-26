from django.urls import path

from .views import CreateCompany

urlpatterns = [
    path(
        "",
        CreateCompany.as_view(),
        name="api_company"
    )
]
