from typing import Optional
from pydantic import BaseModel


class PriceTagValidator(BaseModel):
    """
    Pydantic model for price tag data validation
    on processing post ("new price tag") request
    """

    start_date: str
    end_date: str
    price: float
    description: Optional[str]
