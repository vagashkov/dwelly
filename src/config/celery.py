import os

from celery import Celery
from celery.signals import setup_logging  # noqa

# Obtain access to Django project settings
os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "config.settings.local-dev"
)

# Create and configure Celery app
app = Celery("celery")
app.config_from_object(
    "django.conf:settings",
    namespace="CELERY"
)


# Setup logging using Django logging
@setup_logging.connect
def config_loggers(*args, **kwargs):
    from logging.config import dictConfig  # noqa
    from django.conf import settings  # noqa

    dictConfig(settings.LOGGING)


# Enable shared_tasks autodiscover
app.autodiscover_tasks()


@app.task(bind=True, ignore_result=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
