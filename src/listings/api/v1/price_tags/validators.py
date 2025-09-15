from datetime import datetime
from typing import Optional
from pydantic import BaseModel, field_validator

from ..constants import ERROR_MSG_WRONG_DATE_FORMAT

from ....models import PriceTag


class PriceTagValidator(BaseModel):
    """
    Pydantic model for price tag data validation
    on processing post ("new price tag") request
    """

    start_date: str
    end_date: str
    price: float
    description: Optional[str]

    @field_validator(PriceTag.Field.start_date)
    def validate_start_date(cls, start_date: str) -> str:
        try:
            datetime.strptime(start_date, "%Y-%m-%d")
        except ValueError:
            raise ValueError(ERROR_MSG_WRONG_DATE_FORMAT)
        return start_date

    @field_validator(PriceTag.Field.end_date)
    def validate_end_date(cls, end_date: str) -> str:
        try:
            datetime.strptime(end_date, "%Y-%m-%d")
        except ValueError:
            raise ValueError(ERROR_MSG_WRONG_DATE_FORMAT)
        return end_date
