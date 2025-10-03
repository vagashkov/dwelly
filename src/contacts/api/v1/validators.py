from typing import Optional
from pydantic import field_validator
from pyngo import QueryDictModel

from ...constants import ERROR_NO_COMPANY_FULL_NAME


class CompanyValidator(QueryDictModel):
    """
    Pydantic model for company data validation
    on processing post ("new company") request
    """

    full_name: str
    short_name: str
    license: Optional[str]
    registration: Optional[str]

    @field_validator("full_name")
    @classmethod
    def validate_full_name(cls, value: str) -> str:
        if not value:
            raise ValueError(
                ERROR_NO_COMPANY_FULL_NAME
            )
        return value
