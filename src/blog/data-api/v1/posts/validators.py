from typing import Optional
from pydantic import BaseModel


class PostValidator(BaseModel):
    """
    Pydantic model for blog post data validation
    on processing post ("new blog post") request
    """

    title: str
    excerpt: str
    text: str
    tags: Optional[list] = []
