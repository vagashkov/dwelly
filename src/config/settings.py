"""
Django settings for dwelly project.

"""

from socket import gethostname, gethostbyname_ex

from pathlib import Path
from environs import Env

from ff3 import FF3Cipher

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Load sensitive settings from .env file
env = Env()
env.read_env(BASE_DIR / ".env")

SECRET_KEY: str = env.str("SECRET_KEY")
DEBUG: bool = env.bool("DEBUG", default=False)
FF3_CIPHER = FF3Cipher(
            env.str("FF3_KEY"),
            env.str("FF3_TWEAK")
        )
FF3_LENGTH: int = env.int("FF3_LENGTH", 6)

# DOMAINS section
DOMAIN_NAME: str = env.str("DOMAIN_NAME")
ALLOWED_HOSTS = [
    DOMAIN_NAME,
]

# define internal ips list for debug toolbar with Docker support
hostname, aliases, ips = gethostbyname_ex(gethostname())
INTERNAL_IPS = [
    ".".join(ip.split(".")[:-1] + ["1"]) for ip in ips
]

# Application definition
DJANGO_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

THIRD_PARTY_APPS = [
    # allauth lib support
    "allauth",
    "allauth.account",
    # DRF support
    "rest_framework",
    "rest_framework.authtoken",
    "dj_rest_auth",
    "django_filters",
    "drf_spectacular",
    # UI optimizers
    "crispy_forms",
    "crispy_bootstrap5",
    # development tools
    "debug_toolbar",
]

PROJECT_APPS = [
    "accounts.apps.AccountsConfig",
    "blog.apps.BlogConfig"
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + PROJECT_APPS

MIDDLEWARE = [
    # debug support middleware
    "debug_toolbar.middleware.DebugToolbarMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    # allauth support
    "allauth.account.middleware.AccountMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                # allauth support
                "django.template.context_processors.request",
            ],
        },
    },
]
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

WSGI_APPLICATION = "config.wsgi.application"

# Database
# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.sqlite3",
#         "NAME": BASE_DIR / "db.sqlite3",
#     }
# }
# Database credentials
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": env.str("POSTGRES_DB"),
        "USER": env.str("POSTGRES_USER"),
        "PASSWORD": env.str("POSTGRES_PASSWORD"),
        "HOST": env.str("POSTGRES_HOST"),
        "PORT": env.int("POSTGRES_PORT", 5432)
    }
}

# Authentication parameters
AUTH_USER_MODEL = "accounts.Account"
ACCOUNT_AUTHENTICATION_METHOD = "email"
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_EMAIL_VERIFICATION = "none"
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_USER_MODEL_USERNAME_FIELD = None
LOGIN_REDIRECT_URL = "home"

AUTHENTICATION_BACKENDS = [
    # Needed to login by username in Django admin, regardless of `allauth`
    "django.contrib.auth.backends.ModelBackend",
    # allauth specific authentication methods, such as login by email
    "allauth.account.auth_backends.AuthenticationBackend",
]

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",  # noqa: E501
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",  # noqa: E501
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",  # noqa: E501
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",  # noqa: E501
    },
]

REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.AllowAny",
    ],
    "DEFAULT_AUTHENTICATION_CLASSES": [
        # Uncomment to use standard Django authentication
        "rest_framework.authentication.SessionAuthentication",
        "rest_framework.authentication.TokenAuthentication",
        # Uncomment to use JWT
        # "rest_framework_simplejwt.authentication.JWTAuthentication",
    ],
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "DEFAULT_FILTER_BACKENDS": [
        "django_filters.rest_framework.DjangoFilterBackend",
    ]
}

SPECTACULAR_SETTINGS = {
    "TITLE": "Dwelly project API",
    "DESCRIPTION": "Simple yet functional asset management system for small/family hotel owners",  # noqa: E501
    "VERSION": "1.0.0",
    "SERVE_INCLUDE_SCHEMA": False,
}


# Internationalization
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = "static/"
STATICFILES_DIRS = [
    BASE_DIR / "static"
]

# Media files storage configuration
MEDIA_ROOT = BASE_DIR.parent.joinpath("media")
MEDIA_URL = "/media/"

# Default primary key field type
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
