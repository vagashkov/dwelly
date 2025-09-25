from django.contrib.admin import ModelAdmin, site

from core.models import BaseModel

from .models import (
    Company, CompanyAddress,
    ContactType, CompanyContact,
    Contact
)


class CompanyAdmin(ModelAdmin):
    """
    Manages Company object manipulation using admin panel
    """

    list_display = (
        Company.Field.short_name,
    )


class ContactAdmin(ModelAdmin):
    list_display = (
        BaseModel.Field.created_at,
        Contact.Field.author,
        Contact.Field.is_processed
    )
    list_filter = (
        Contact.Field.is_processed,
    )


site.register(Company, CompanyAdmin)
site.register(ContactType)
site.register(CompanyContact)
site.register(CompanyAddress)
site.register(Contact, ContactAdmin)
