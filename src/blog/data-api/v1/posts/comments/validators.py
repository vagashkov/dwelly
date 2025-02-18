from pydantic import BaseModel


class CommentValidator(BaseModel):
    """
    Pydantic model for post comment data validation
    on processing post ("new blog post comment") request
    """

    text: str
