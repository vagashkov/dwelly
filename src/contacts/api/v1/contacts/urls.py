from django.urls import path, include

# from .views import CreateCompany

urlpatterns = [
    path(
        "contact_types/",
        include("contacts.api.v1.contacts.types.urls")
    ),
    # path(
    #     "",
    #     CreateCompany.as_view(),
    #     name="api_company"
    # )
]
