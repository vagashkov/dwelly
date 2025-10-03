from typing import Optional

from pydantic import field_validator
from pyngo import QueryDictModel

from ....constants import (
    ERROR_NO_CONTACT_VALUE,
    ERROR_WRONG_CONTACT_TYPE_ID,
    ERROR_WRONG_COMPANY_ID
)
from ....models import (
    Company, CompanyContact, ContactType
)


class ContactValidator(QueryDictModel):
    """
    Pydantic model for contact validation
    on processing post ("new contact") request
    """

    contact_type: int
    company: int
    value: str
    description: Optional[str]

    @field_validator(CompanyContact.Field.contact_type)
    def check_contact_type(cls, contact_type: int) -> int:
        try:
            ContactType.objects.get(id=contact_type)
            return contact_type
        except ContactType.DoesNotExist:
            raise ValueError(
                ERROR_WRONG_CONTACT_TYPE_ID.format(
                    contact_type
                )
            )

    @field_validator(CompanyContact.Field.value)
    def check_contact_value(cls, value: str) -> str:
        if not value:
            raise ValueError(
                ERROR_NO_CONTACT_VALUE
            )
        return value

    @field_validator(CompanyContact.Field.company)
    def check_company(cls, company: int) -> int:
        try:
            Company.objects.get(id=company)
            return company
        except Company.DoesNotExist:
            raise ValueError(
                ERROR_WRONG_COMPANY_ID.format(
                    company
                )
            )
