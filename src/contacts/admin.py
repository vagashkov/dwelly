from django.contrib.admin import ModelAdmin, site

from core.models import BaseModel

from .models import (
    Company, CompanyAddress,
    ContactType, CompanyContact,
    UserMessage
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
        UserMessage.Field.author,
        UserMessage.Field.is_processed
    )
    list_filter = (
        UserMessage.Field.is_processed,
    )


site.register(Company, CompanyAdmin)
site.register(ContactType)
site.register(CompanyContact)
site.register(CompanyAddress)
site.register(UserMessage, ContactAdmin)
