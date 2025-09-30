from typing import Optional

from pyngo import QueryDictModel


class ContactValidator(QueryDictModel):
    """
    Pydantic model for contact validation
    on processing post ("new contact") request
    """

    contact_type: str
    value: str
    description: Optional[str]
