from typing import List
from pyngo import QueryDictModel


class PostValidator(QueryDictModel):
    """
    Pydantic model for blog post data validation
    on processing post ("new blog post") request
    """

    title: str
    excerpt: str
    text: str
    tags: List[int]
