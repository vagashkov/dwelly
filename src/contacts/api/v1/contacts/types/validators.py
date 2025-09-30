from pyngo import QueryDictModel


class ContactTypeValidator(QueryDictModel):
    """
    Pydantic model for contact type validation
    on processing post ("new contact type") request
    """

    name: str
    description: str
