"""
Shared django settings.
"""
import os
from os.path import join

import dj_database_url
from distutils.util import strtobool

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ------------------------------------------------------------------------------------------------------------------
import environ
env = environ.Env(
    DEBUG=(bool, False)
)
# reading .env file
environ.Env.read_env()

# overwrite environment variables with local .env settings
if "PKDB_SECRET_KEY" in env:
    os.environ["PKDB_SECRET_KEY"] = env("PKDB_SECRET_KEY")
if "PKDB_API_BASE" in env:
    os.environ["PKDB_API_BASE"] = env("PKDB_API_BASE")
if "PKDB_DEFAULT_PASSWORD" in env:
    os.environ["PKDB_DEFAULT_PASSWORD"] = env("PKDB_DEFAULT_PASSWORD")
if "PKDB_POSTGRES_PASSWORD" in env:
    os.environ["PKDB_POSTGRES_PASSWORD"] = env("PKDB_POSTGRES_PASSWORD")

# either 'Local' or 'Production'
DJANGO_CONFIGURATION = os.getenv("PKDB_DJANGO_CONFIGURATION", "Local")
SECRET_KEY = os.getenv("PKDB_SECRET_KEY")
API_BASE = os.getenv("PKDB_API_BASE")
DEFAULT_PASSWORD = os.getenv("PKDB_DEFAULT_PASSWORD")

if not SECRET_KEY:
    raise ValueError("SECRET_KEY could not be read, export the 'PKDB_SECRET_KEY' environment variable.")
if not DEFAULT_PASSWORD:
    raise ValueError("DEFAULT_PASSWORD could not be read, export the 'PKDB_DEFAULT_PASSWORD' environment variable.")
if not API_BASE:
    raise ValueError("API_BASE could not be read, export the 'PKDB_API_BASE' environment variable.")

API_URL = API_BASE + "/api/v1"
# ------------------------------------------------------------------------------------------------------------------

AUTHENTICATION_BACKENDS = (

    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',

    # `allauth` specific authentication methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend',
)


INSTALLED_APPS = (
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.sites",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # Authentication
    'bootstrap3',  # optional module for making bootstrap forms easier

    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.github',
    #'allauth.socialaccount.providers.google',

    # Third party apps
    "rest_framework",  # utilities for rest apis
    "rest_framework.authtoken",  # token authentication
    "django_filters",  # for filtering rest endpoints
    "rest_framework_swagger",
    "corsheaders",

    # Your apps
    "pkdb_app.users",
    "pkdb_app.studies",
    "pkdb_app.subjects",
    "pkdb_app.interventions",
    "pkdb_app.comments",
)

SITE_ID = 1
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_MIN_LENGTH = 3

SOCIALACCOUNT_PROVIDERS = {
    'github': {
        'SCOPE': ['email'],
        'METHOD': 'oauth2',
    },
    # 'google':
    #     { 'SCOPE': ['profile', 'email'],
    #       'AUTH_PARAMS': {'access_type': 'online'}
    #     },

}

# https://docs.djangoproject.com/en/2.0/topics/http/middleware/
MIDDLEWARE = (
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
)

CORS_ORIGIN_WHITELIST = (
    "0.0.0.0:8081",
    "localhost:8081",
    "0.0.0.0:8080",
    "localhost:8080",
)
INTERNAL_IPS = ("172.18.0.1",)

ALLOWED_HOSTS = ["*"]
ROOT_URLCONF = "pkdb_app.urls"

WSGI_APPLICATION = "pkdb_app.wsgi.application"

# Email
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"

ADMINS = (("Author", "janekg89@hotmail.de"),)

# General
APPEND_SLASH = False
TIME_ZONE = "UTC"
LANGUAGE_CODE = "en-us"
# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = False
USE_L10N = True
USE_TZ = True
LOGIN_REDIRECT_URL = "/"

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/
STATIC_ROOT = os.path.normpath(join(os.path.dirname(BASE_DIR), "static"))
STATICFILES_DIRS = [os.path.join(BASE_DIR, "static"), os.path.join(BASE_DIR, "pkdb_app", "static")]
STATIC_URL = "/static/"
STATICFILES_FINDERS = (
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
)

# Media files
MEDIA_ROOT = join(os.path.dirname(BASE_DIR), "media")
MEDIA_URL = "/media/"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": STATICFILES_DIRS + [os.path.join(BASE_DIR, "pkdb_app", "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [

                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ]
        },
    }
]

# Custom user app
AUTH_USER_MODEL = "users.User"


# Password Validation
# https://docs.djangoproject.com/en/2.0/topics/auth/passwords/#module-django.contrib.auth.password_validation
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# Logging
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "django.server": {
            "()": "django.utils.log.ServerFormatter",
            "format": "[%(server_time)s] %(message)s",
        },
        "verbose": {
            "format": "%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s"
        },
        "simple": {"format": "%(levelname)s %(message)s"},
    },
    "filters": {"require_debug_true": {"()": "django.utils.log.RequireDebugTrue"}},
    "handlers": {
        "django.server": {
            "level": "INFO",
            "class": "logging.StreamHandler",
            "formatter": "django.server",
        },
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "simple",
        },
        "mail_admins": {
            "level": "ERROR",
            "class": "django.utils.log.AdminEmailHandler",
        },
    },
    "loggers": {
        "django": {"handlers": ["console"], "propagate": True},
        "django.server": {
            "handlers": ["django.server"],
            "level": "INFO",
            "propagate": False,
        },
        "django.request": {
            "handlers": ["mail_admins", "console"],
            "level": "ERROR",
            "propagate": False,
        },
        "django.db.backends": {"handlers": ["console"], "level": "INFO"},
    },
}

# Django Rest Framework
REST_FRAMEWORK = {
    # 'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    "DEFAULT_PAGINATION_CLASS": "pkdb_app.pagination.CustomPagination",
    "PAGE_SIZE": int(os.getenv("DJANGO_PAGINATION_LIMIT", 10)),
    "DATETIME_FORMAT": "%Y-%m-%dT%H:%M:%S%z",
    "DEFAULT_RENDERER_CLASSES": (
        "rest_framework.renderers.JSONRenderer",
        "rest_framework.renderers.BrowsableAPIRenderer",
    ),
    "DEFAULT_PERMISSION_CLASSES": ["rest_framework.permissions.AllowAny"],
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework.authentication.SessionAuthentication",
        "rest_framework.authentication.TokenAuthentication",
    ),
    "DEFAULT_FILTER_BACKENDS": (
        "django_filters.rest_framework.DjangoFilterBackend",
    ),
}
LOGIN_URL = "rest_framework:login"
LOGOUT_URL = "rest_framework:logout"

SWAGGER_SETTINGS = {
    "LOGIN_URL": "rest_framework:login",
    "LOGOUT_URL": "rest_framework:logout",
    "USE_SESSION_AUTH": True,
    "DOC_EXPANSION": "list",
    "APIS_SORTER": "alpha",
    "SECURITY_DEFINITIONS": {"basic": {"type": "basic"}},
}


# Set DEBUG to False as a default for safety
# https://docs.djangoproject.com/en/dev/ref/settings/#debug
DEBUG = strtobool(os.getenv("DJANGO_DEBUG", "no"))
# ------------------------------
# LOCAL
# ------------------------------
if DJANGO_CONFIGURATION == 'Local':
    DEBUG = True

    # Postgres
    DATABASES = {
        "default": dj_database_url.config(
            # postgres://USER:PASSWORD@HOST:PORT/NAME
            default=f"postgres://postgres:pass@postgres:5432/postgres",
            conn_max_age=int(os.getenv("POSTGRES_CONN_MAX_AGE", 600)),
        )
    }

    # DATABASES = {
    #    'default': {
    #        'ENGINE': 'django.db.backends.sqlite3',
    #        'NAME': 'test',
    #    }
    # }

    # Mail
    EMAIL_HOST = "localhost"
    EMAIL_PORT = 1025
    EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# -------------------------------------------------
# Production
# -------------------------------------------------
elif DJANGO_CONFIGURATION == 'Production':
    DEBUG = False

    POSTGRES_PASSWORD = os.getenv("PKDB_POSTGRES_PASSWORD")

    # Postgres
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": "pkdb",
            "USER": "pkdb_user",
            "HOST": "localhost",
            "PASSWORD": POSTGRES_PASSWORD,
            "PORT": 5432,
        }
    }

    # Site
    # https://docs.djangoproject.com/en/2.0/ref/settings/#allowed-hosts
    INSTALLED_APPS += ("gunicorn",)
else:
    raise ValueError(f"Unsupported DJANGO_CONFIGURATION: {DJANGO_CONFIGURATION}")
