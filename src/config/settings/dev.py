from ff3 import FF3Cipher

from .base import *  # noqa: F401, F403

DEBUG = True
ALLOWED_HOSTS = []
SECRET_KEY = "django-insecure-hz^x4#xvj7p@6p2h64ssh9*uccr-7ecjcmi2944!pf!sk6&e%@"  # noqa: E501

# Database connection credentials
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "pethotel-dev",
        "USER": "pethotel",
        "PASSWORD": "pethotel",
        "HOST": "localhost",
        "PORT": 5432
    }
}

# FF3 encrypter settings (read https://pypi.org/project/ff3/ for details)
FF3_KEY = "C4A5CEFE80FA957333EA7947AC284467"
FF3_TWEAK = "01D250AAD1B8B6"
FF3_LENGTH = 6
FF3_CIPHER = FF3Cipher(FF3_KEY, FF3_TWEAK)

# Static files (CSS, JavaScript, Images)
STATIC_URL = "static/"
STATICFILES_DIRS = [
    BASE_DIR / "static"
]

