from .base import *  # noqa: F401, F403

DEBUG = True
ALLOWED_HOSTS = []
SECRET_KEY = "django-insecure-hz^x4#xvj7p@6p2h64ssh9*uccr-7ecjcmi2944!pf!sk6&e%@"  # noqa: E501

# Database connection credentials
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "postgres",
        "USER": "postgres",
        "PASSWORD": "postgres",
        "HOST": "db",
        "PORT": 5432
    }
}
