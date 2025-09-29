from pyngo import QueryDictModel


class AddressValidator(QueryDictModel):
    """
    Pydantic model for address validation
    on processing post ("new company") request
    """

    country: str
    city: str
    street_address: str
    zip_code: str
