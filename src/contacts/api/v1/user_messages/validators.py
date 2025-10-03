from pydantic import field_validator
from pyngo import QueryDictModel

from ....constants import (
    ERROR_NO_AUTHOR_NAME,
    ERROR_WRONG_CONTACT_TYPE_ID,
    ERROR_NO_AUTHOR_CONTACT,
    ERROR_NO_TEXT
)
from ....models import ContactType, UserMessage


class UserMessageValidator(QueryDictModel):
    """
    Pydantic model for user messages validation
    on processing post ("new user message") request
    """

    author: str
    contact_type: int
    contact: str
    text: str

    @field_validator(UserMessage.Field.author)
    def check_author(cls, author: str) -> str:
        if not author:
            raise ValueError(
                ERROR_NO_AUTHOR_NAME
            )
        return author

    @field_validator(UserMessage.Field.contact_type)
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

    @field_validator(UserMessage.Field.contact)
    def check_contact(cls, contact: str) -> str:
        if not contact:
            raise ValueError(
                ERROR_NO_AUTHOR_CONTACT
            )
        return contact

    @field_validator(UserMessage.Field.text)
    def check_text(cls, text: str) -> str:
        if not text:
            raise ValueError(
                ERROR_NO_TEXT
            )
        return text
