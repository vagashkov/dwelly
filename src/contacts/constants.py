from django.utils.translation import gettext_lazy as _

from core.models import BaseModel

ACTIVE_POST_STATUS = "Published"
POSTS_ORDERING = "-{}".format(BaseModel.Field.created_at)
COMMENTS_ORDERING = "{}".format(BaseModel.Field.created_at)

ERROR_KEY = "errors"
ERROR_MSG_NO_INITIAL_STATUS = _("Initial status not found")
ERROR_MSG_NO_IMAGE_ATTACHED = _("Image is not attached")
ERROR_MSG_NO_POST = _("Post not found")
ERROR_MSG_NO_POST_SLUG = _("Post slug not found")
ERROR_MSG_MULTIPLE_POSTS = _("Multiple posts found: {}")
ERROR_MSG_UNSUPPORTED_IMAGE_FORMAT = _(
    "Unsupported image format. JPEG/PNG needed"
    )
