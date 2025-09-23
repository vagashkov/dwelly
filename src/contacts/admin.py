from django.contrib.admin import ModelAdmin, site

from .models import (
    Company, CompanyAddress,
    ContactType, CompanyContact
)


class CompanyAdmin(ModelAdmin):
    """
    Manages Company object manipulation using admin panel
    """

    list_display = (
        Company.Field.short_name,
    )


site.register(Company, CompanyAdmin)
site.register(ContactType)
site.register(CompanyContact)
site.register(CompanyAddress)
