from typing import Optional
from pydantic import BaseModel, Field, field_validator

from ...constants import (
    ERROR_MSG_UNKNOWN_AMENITIES,
    ERROR_MSG_UNKNOWN_HOUSE_RULES
)
from ...models import Amenity, HouseRule, Listing


class PostListing(BaseModel):
    """
    Pydantic model for listing data validation
    on processing post ("new listing") request
    """

    # Base info
    object_type: int
    title: str
    description: Optional[str]
    # Capacity
    max_guests: int = Field(ge=1)
    bedrooms: int = Field(ge=1)
    beds: int = Field(ge=1)
    bathrooms: int = Field(ge=0)
    # Add-ons
    amenities: list[int]
    house_rules: list[int]
    # Reservation
    check_in_time: str
    check_out_time: str
    instant_booking: bool

    @field_validator(Listing.Field.amenities)
    def check_amenities(cls, amenities: list[int]) -> list[int]:
        lost_ids = list()
        for amenity in amenities:
            try:
                Amenity.objects.get(id=amenity)
            except Amenity.DoesNotExist:
                lost_ids.append(amenity)
        if lost_ids:
            raise ValueError(
                ERROR_MSG_UNKNOWN_AMENITIES.format(lost_ids)
                )
        return amenities

    @field_validator(Listing.Field.house_rules)
    def check_house_rules(cls, house_rules: list[int]) -> list[int]:
        lost_ids = list()
        for rule in house_rules:
            try:
                HouseRule.objects.get(id=rule)
            except HouseRule.DoesNotExist:
                lost_ids.append(rule)
        if lost_ids:
            raise ValueError(
                ERROR_MSG_UNKNOWN_HOUSE_RULES.format(lost_ids)
            )
        return house_rules
