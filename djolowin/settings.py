import os
import ast
import warnings
import sentry_sdk
import stripe

from datetime import timedelta
from dotenv import load_dotenv
from sentry_sdk.integrations.django import DjangoIntegration
from sentry_sdk.integrations.celery import CeleryIntegration
from pathlib import Path

from core.languages import LANGUAGES as CORE_LANGUAGES

load_dotenv()
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

APPEND_SLASH = False

# Tell Django about the custom `User` model we created. The string
# `account.User` tells Django we are referring to the `CustomUser` model in
# the `account` module. This module is registered above in a setting
# called `INSTALLED_APPS`.
AUTH_USER_MODEL = "custom_user.CustomUser"

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = str(os.environ.get("SECRET_KEY"))
ENCRYPT_KEY = os.environ.get("ENCRYPT_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
ALLOWED_HOSTS = [
    "*",
]
ALLOWED_CLIENT_HOSTS = ["*"]

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.humanize",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",
    # Third party apps
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "allauth.socialaccount.providers.google",
    "celery",
    "corsheaders",
    "custom_user",
    "django_countries",
    "django_extensions",
    "django_filters",
    "django_redis",
    "graphene_django",
    "phonenumber_field",
    "rest_framework",
    "rest_framework.authtoken",
    "rest_framework_simplejwt",
    "rest_framework_simplejwt.token_blacklist",
    # local apps
    "analytics",
    "app_currency",
    "auction",
    "card",
    "core",
    "djolowin_graphql",
    "djolowin_profile",
    "marketplace",
    "notification",
    "order",
    "permission",
    "product",
    "ranking",
    "reward",
    "sports",
    "transaction",
]


MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
]
CSRF_TRUSTED_ORIGINS = ["http://127.0.0.1", "http://192.168.1.190"]

ROOT_URLCONF = "djolowin.urls"


context_processors = [
    "django.template.context_processors.debug",
    "django.template.context_processors.request",
    "django.contrib.auth.context_processors.auth",
    "django.contrib.messages.context_processors.messages",
]
TEMPLATE_DIR = os.path.join(BASE_DIR, "templates")
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [TEMPLATE_DIR],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": context_processors,
        },
    },
]

WSGI_APPLICATION = "djolowin.wsgi.application"


BASE_URL = "http://localhost:8000"
SITE_ID = 1

# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db/primary_db.sqlite3",
    },
    "auction_db": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db/auction_db.sqlite3",
    },
    "card_db": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db/card_db.sqlite3",
    },
    "vcurrency_db": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db/vcurrency_db.sqlite3",
    },
    "notification_db": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db/notification_db.sqlite3",
    },
    "product_db": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db/product_db.sqlite3",
    },
    "sports_db": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db/sports_db.sqlite3",
    },
    "transaction_db": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db/transaction_db.sqlite3",
    },
}

DATABASE_ROUTERS = [
    "app_currency.routers.AppCurrencyRouter",
    "auction.routers.AuctionRouter",
    "card.routers.CardRouter",
    "notification.routers.NotificationRouter",
    "product.routers.ProductRouter",
    "sports.routers.SportsRouter",
    "reward.routers.RewardRouter",
    "transaction.routers.TransactionRouter",
]

# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# JWT settings
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ],
}

AUTH_COOKIE = "access_token"
JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=1)

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": JWT_ACCESS_TOKEN_EXPIRES,
    "REFRESH_TOKEN_LIFETIME": JWT_REFRESH_TOKEN_EXPIRES,
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
    "ALGORITHM": "HS256",
    "SIGNING_KEY": str(os.environ.get("SIGNING_JWT_KEY")),
    "AUTH_HEADER_TYPES": ("JWT",),
    "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.AccessToken",),
    "TOKEN_TYPE_CLAIM": "token_type",
    "TOKEN_BLACKLIST_ENABLED": True,
}


AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
]

# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = "en"
LANGUAGES = CORE_LANGUAGES

TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True


# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"# URL that handles the media
# served \from MEDIA_ROOT. Make sure to use a
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = os.environ.get("MEDIA_URL", "/media/")


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/
STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]

STATIC_URL = "/static/"
DJOLOWIN_STATIC_BASE_URL = "/static/"
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


LOGOUT_REDIRECT_URL = "account:login"
LOGIN_REDIRECT_URL = "http://localhost:8080/home"
LOGIN_URL = "account:login"
LOGOUT_URL = "account:logout"

APPEND_SLASH = True
DJOLOWIN_ACCOUNTS_REDIRECT_URL = "account:user-detail"

# Defaults variables\
DJOLOWIN_FRONTEND_URL = "http://localhost:8080"
DATABASE_CONNECTION_DEFAULT_NAME = os.environ.get("DB_NAME")
DEFAULT_FROM_EMAIL = "monsieurdjolo@djolo.win"
DEFAULT_CURRENCY = "cad"
DEFAULT_CURRENCY_CODE_LENGTH = 3
DEFAULT_DECIMAL_PLACES = 2
DEFAULT_MAX_DIGITS = 12
DEFAULT_CURRENCY_CODE_LENGTH = 3
DJOLOWIN_PLAYERCARD_PAGINATE_BY = 40
DJOLOWIN_NOTIFICATIONS_PER_PAGE = 20
DJOLOWIN_SAVE_SENT_EMAILS_TO_DB = True
LOGIN_ATTEMPTS_TIMEOUT = 60 * 5  # 5 minutes
MAX_LOGIN_ATTEMPTS = 5

# Email server configuration
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST = "smtp-mail.outlook.com"
EMAIL_HOST_USER = "test@test.com"
EMAIL_HOST_PASSWORD = "test1234"


# Password reset settings
# Number of days a password reset link is valid
PASSWORD_RESET_TIMEOUT_DAYS = 1

# Email subject for password reset emails
PASSWORD_RESET_SUBJECT = "Reset your password on DjoloWin"

# Email body for password reset emails
PASSWORD_RESET_EMAIL_TEMPLATE = "djolowin/account/password_reset_email.html"

EMAIL_TEMPLATE_NAME = "djolowin/account/password_reset_email.html"

# Stripe settings for payment gateway
STRIPE_SECRET_KEY = os.environ.get("STRIPE_SECRET_KEY")
STRIPE_PUBLISHABLE_KEY = os.environ.get("STRIPE_PUBLISHABLE_KEY")
STRIPE_WEBHOOK_SECRET = os.environ.get("STRIPE_WEBHOOK_SECRET")
stripe.api_key = STRIPE_SECRET_KEY

# CORS settings
CORS_ALLOW_ALL_ORIGINS = False
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOWED_ORIGINS = ["http://localhost:8080", "http://192.168.1.190:8080"]

JWT_EXPIRE = 60 * 60 * 24 * 7  # 7 days


# Celery settings for background tasks
CELERY_BROKER_URL = "redis://localhost:6379"
CELERY_RESULT_BACKEND = "redis://localhost:6379"
CELERY_ACCEPT_CONTENT = ["application/json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"
CELERY_TIMEZONE = "UTC"


# GraphQL settings
GRAPHENE = {
    "SCHEMA": "djolowin_graphql.api.schema",
    "ATOMIC_MUTATIONS": True,
}

ENABLE_SSL = False


# Allauth settings
# Additional configuration settings
ACCOUNT_AUTHENTICATION_METHOD = "email"
ACCOUNT_LOGOUT_ON_GET = True
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_MAX_EMAIL_ADDRESSES = 1
ACCOUNT_EMAIL_VERIFICATION = "optional"

# Email confirmation
ACCOUNT_EMAIL_SUBJECT_PREFIX = "DjoloWin: "
ACCOUNT_LOGIN_ON_EMAIL_CONFIRMATION = True

# After 10 failed login attempts, restrict logins for 30 minutes
ACCOUNT_LOGIN_ATTEMPTS_LIMIT = 10
ACCOUNT_LOGIN_ATTEMPTS_TIMEOUT = 1800
ACCOUNT_PASSWORD_MIN_LENGTH = 12

# Other settings
# ACCOUNT_DEFAULT_HTTP_PROTOCOL = "https"
ACCOUNT_LOGIN_ON_PASSWORD_RESET = True
SOCIALACCOUNT_AUTO_SIGNUP = False


SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'APP': {
            'client_id': os.environ.get("GOOGLE_CLIENT_ID"),
            'secret': os.environ.get("GOOGLE_CLIENT_SECRET"),
            'key': ''
        },
        'SCOPE': [
            'profile',
            'email',
        ],
        'AUTH_PARAMS': {
            'access_type': 'offline',
        }
    }
}


CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/1",  # Update with your Redis server details
        "TIMEOUT": 180,
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        },
    }
}

CACHE_TTL = 60
