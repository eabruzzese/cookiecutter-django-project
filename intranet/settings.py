"""
Django settings for intranet project.

Generated by 'django-admin startproject' using Django 4.1.3.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""

from email.utils import parseaddr
from pathlib import Path

import environ

env = environ.Env()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Read the .env file (if it exists)
env.read_env(BASE_DIR / ".env")


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env("DEBUG", default=False)

ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=[])
USE_X_FORWARDED_HOST = env("USE_X_FORWARDED_HOST", default=True)

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.sites",
    "django.contrib.staticfiles",
    # First-party apps
    "intranet.accounts",
    # Third-party apps
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "django_otp",
    "django_otp.plugins.otp_totp",
    "django_otp.plugins.otp_static",
    "constance",
    "constance.backends.database",
    "corsheaders",
    "debug_toolbar",
    "django_extensions",
    "django_celery_results",
    "django_celery_beat",
    "health_check",
    "health_check.db",
    "health_check.cache",
    "health_check.storage",
    "health_check.contrib.migrations",
    "health_check.contrib.celery",
    "health_check.contrib.psutil",
    "waffle",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "waffle.middleware.WaffleMiddleware",
    "debug_toolbar.middleware.DebugToolbarMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "intranet.accounts.middleware.TimeZoneMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "intranet.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            BASE_DIR / "intranet" / "templates",
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "intranet.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases
DATABASE_URL = env.url("DATABASE_URL")

# Special handling to support project-relative SQLite paths.
# See: https://github.com/joke2k/django-environ/issues/187
if DATABASE_URL.scheme == "sqlite" and DATABASE_URL.netloc:
    DATABASE_FILE_PATH = str((BASE_DIR / ".." / DATABASE_URL.netloc).resolve())
    DATABASE_URL = DATABASE_URL._replace(netloc="", path=f"/{DATABASE_FILE_PATH}")

DATABASES = {
    # Parse the DATABASE_URL from the environment and create a database
    # configuration from it.
    "default": env.db_url_config(DATABASE_URL)
}

# Cache
# https://docs.djangoproject.com/en/4.1/ref/settings/#caches
CACHE_URL = env.url("CACHE_URL")
CACHES = {
    # Parse the CACHE_URL from the environment and create a cache configuration
    # from it.
    "default": env.cache_url_config(CACHE_URL),
}

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


# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = (BASE_DIR / "intranet" / "static",)
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

AUTH_USER_MODEL = "accounts.User"

SITE_ID = 1

SILENCED_SYSTEM_CHECKS = env.list("SILENCED_SYSTEM_CHECKS", default=[])

LOGOUT_REDIRECT_URL = "account_login"

AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
]

# Email
# https://docs.djangoproject.com/en/4.1/topics/email/
EMAIL_SUBJECT_PREFIX = env("EMAIL_SUBJECT_PREFIX", default="[Intranet] ")
DEFAULT_FROM_EMAIL = env("DEFAULT_FROM_EMAIL", default="Intranet <no-reply@intranet.local>")
SERVER_EMAIL = env("SERVER_EMAIL", default=DEFAULT_FROM_EMAIL)
ADMINS = env.list(
    "ADMINS",
    cast=parseaddr,
    default=[("Intranet Admins", "admins@intranet")],
)
MANAGERS = env.list(
    "MANAGERS", cast=parseaddr, default=[("Inteanet Managers", "managers@intranet.local")]
)

# Parse the configured EMAIL_URL into proper Django settings.
vars().update(env.email_url("EMAIL_URL"))

# Celery
# https://docs.celeryq.dev/en/stable/userguide/configuration.html
CELERY_BROKER_URL = env.url("CELERY_BROKER_URL").geturl()
CELERY_ACCEPT_CONTENT = ["json"]
CELERY_RESULT_BACKEND = "django-db"
CELERY_RESULT_EXTENDED = True
CELERY_TASK_SERIALIZER = "json"
CELERY_TASK_IGNORE_RESULT = env("CELERY_TASK_IGNORE_RESULT", default=True)
CELERY_TASK_STORE_ERRORS_EVEN_IF_IGNORED = True
CELERY_TASK_TRACK_STARTED = env("CELERY_TASK_TRACK_STARTED", default=True)
CELERY_DISABLE_RATE_LIMITS = env("CELERY_DISABLE_RATE_LIMITS", default=True)
CELERY_WORKER_CONCURRENCY = env("CELERY_WORKER_CONCURRENCY", default=12)
CELERY_WORKER_MAX_TASKS_PER_CHILD = env("CELERY_WORKER_MAX_TASKS_PER_CHILD", default=12)
CELERY_WORKER_MAX_MEMORY_PER_CHILD = env("CELERY_WORKER_MAX_MEMORY_PER_CHILD", default=(128 * 1024))
CELERY_BEAT_SCHEDULER = "django_celery_beat.schedulers:DatabaseScheduler"

# Allow the debug toolbar to be toggled with an environment variable.
DEBUG_TOOLBAR_ENABLED = env("DEBUG_TOOLBAR_ENABLED", default=DEBUG)
DEBUG_TOOLBAR_CONFIG = {"SHOW_TOOLBAR_CALLBACK": lambda _: DEBUG_TOOLBAR_ENABLED}

# Constance
# https://django-constance.readthedocs.io/en/latest/
CONSTANCE_BACKEND = "constance.backends.database.DatabaseBackend"
CONSTANCE_DATABASE_CACHE_BACKEND = "default"
CONSTANCE_CONFIG: dict[str, tuple] = {
    "ACCOUNTS_REGISTRATION_OPEN": (
        env("ACCOUNTS_REGISTRATION_OPEN", default=False),
        "Allow registration of new user accounts",
        bool,
    ),
}
CONSTANCE_CONFIG_FIELDSETS: dict[str, tuple] = {}

# Allauth
# https://django-allauth.readthedocs.io/en/latest/configuration.html
ACCOUNT_ADAPTER = "intranet.accounts.adapters.AccountAdapter"
ACCOUNT_DEFAULT_HTTP_PROTOCOL = env("ACCOUNT_DEFAULT_HTTP_PROTOCOL", default="https")
ACCOUNT_AUTHENTICATION_METHOD = "email"
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_PRESERVE_USERNAME_CASING = False
ACCOUNT_SIGNUP_PASSWORD_ENTER_TWICE = False
ACCOUNT_LOGOUT_ON_GET = True
ACCOUNT_AUTHENTICATED_LOGIN_REDIRECTS = False
ACCOUNT_LOGIN_ON_EMAIL_CONFIRMATION = True
ACCOUNT_CONFIRM_EMAIL_ON_GET = True
ACCOUNT_LOGIN_ON_PASSWORD_RESET = True

# Use a custom signup form (for ReCAPTCHA integration).
ACCOUNT_FORMS = {"signup": "intranet.accounts.forms.SignupForm"}
ACCOUNT_LOGIN_ATTEMPTS_LIMIT = env("ACCOUNT_LOGIN_ATTEMPTS_LIMIT", default=5)
ACCOUNT_LOGIN_ATTEMPTS_TIMEOUT = env("ACCOUNT_LOGIN_ATTEMPTS_TIMEOUT", default=300)
OTP_ADMIN_HIDE_SENSITIVE_DATA = True

# ReCAPTCHA
# https://github.com/torchbox/django-recaptcha
RECAPTCHA_PUBLIC_KEY = env("RECAPTCHA_PUBLIC_KEY")
RECAPTCHA_PRIVATE_KEY = env("RECAPTCHA_PRIVATE_KEY")
RECAPTCHA_DOMAIN = env("RECAPTCHA_DOMAIN", default="www.google.com")

# CORS configuration.
# https://github.com/adamchainz/django-cors-headers
CORS_ALLOWED_ORIGINS = env.list("CORS_ALLOWED_ORIGINS", default=[])
CORS_ALLOW_ALL_ORIGINS = env.bool("CORS_ALLOW_ALL_ORIGINS", default=DEBUG)
