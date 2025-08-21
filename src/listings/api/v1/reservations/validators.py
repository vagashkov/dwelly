from datetime import datetime
from typing import Optional
from pydantic import BaseModel, field_validator

from ....models import Reservation

from ..constants import ERROR_MSG_WRONG_DATE_FORMAT


class ReservationValidator(BaseModel):
    """
    Pydantic model for reservation data validation
    on processing post ("new reservation") request
    """

    check_in: str
    check_out: str
    comment: Optional[str]

    @field_validator(Reservation.Field.check_in)
    def validate_start_date(cls, check_in: str) -> str:
        try:
            datetime.strptime(check_in, "%Y-%m-%d")
        except ValueError:
            raise ValueError(ERROR_MSG_WRONG_DATE_FORMAT)
        return check_in

    @field_validator(Reservation.Field.check_out)
    def validate_end_date(cls, check_out: str) -> str:
        try:
            datetime.strptime(check_out, "%Y-%m-%d")
        except ValueError:
            raise ValueError(ERROR_MSG_WRONG_DATE_FORMAT)
        return check_out
