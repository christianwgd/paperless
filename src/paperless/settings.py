"""
Django settings for paperless project.

Generated by 'django-admin startproject' using Django 1.9.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.10/ref/settings/
"""

import json
import os
import re

from dotenv import load_dotenv


# Tap paperless.conf if it's available
if os.path.exists("/etc/paperless.conf"):
    load_dotenv("/etc/paperless.conf")
elif os.path.exists("/usr/local/etc/paperless.conf"):
    load_dotenv("/usr/local/etc/paperless.conf")


def __get_boolean(key, default="NO"):
    """
    Return a boolean value based on whatever the user has supplied in the
    environment based on whether the value "looks like" it's True or not.
    """
    return bool(
        os.getenv(key, default).lower() in ("yes", "y", "1", "t", "true")
    )


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/

# The secret key has a default that should be fine so long as you're hosting
# Paperless on a closed network.  However, if you're putting this anywhere
# public, you should change the key to something unique and verbose.
SECRET_KEY = os.getenv(
    "PAPERLESS_SECRET_KEY",
    "e11fl1oa-*ytql8p)(06fbj4ukrlo+n7k&q5+$1md7i+mge=ee"
)


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = __get_boolean("PAPERLESS_DEBUG", "YES")

LOGIN_URL = "admin:login"

ALLOWED_HOSTS = ["*"]

_allowed_hosts = os.getenv("PAPERLESS_ALLOWED_HOSTS")
if _allowed_hosts:
    ALLOWED_HOSTS = _allowed_hosts.split(",")

FORCE_SCRIPT_NAME = os.getenv("PAPERLESS_FORCE_SCRIPT_NAME")

# Application definition

INSTALLED_APPS = [
    "whitenoise.runserver_nostatic",

    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    "corsheaders",
    "django_extensions",

    "paperless",
    "documents.apps.DocumentsConfig",
    "reminders.apps.RemindersConfig",
    "paperless_tesseract.apps.PaperlessTesseractConfig",
    "paperless_text.apps.PaperlessTextConfig",

    "django.contrib.admin",

    "rest_framework",
    "crispy_forms",
    "django_filters",
    "djangoql",

    'bootstrap4',
]

if os.getenv("PAPERLESS_INSTALLED_APPS"):
    INSTALLED_APPS += os.getenv("PAPERLESS_INSTALLED_APPS").split(",")

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# Enable whitenoise compression and caching
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# We allow CORS from localhost:8000
CORS_ALLOWED_ORIGINS = tuple(os.getenv(
    "PAPERLESS_CORS_ALLOWED_HOSTS",
    "http://localhost:8000,https://localhost:8000"
).split(","))


# If auth is disabled, we just use our "bypass" authentication middleware
if bool(os.getenv("PAPERLESS_DISABLE_LOGIN", "false").lower() in ("yes", "y", "1", "t", "true")):
    _index = MIDDLEWARE.index("django.contrib.auth.middleware.AuthenticationMiddleware")
    MIDDLEWARE[_index] = "paperless.middleware.Middleware"

ROOT_URLCONF = 'paperless.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'paperless.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.path.join(
            os.getenv(
                "PAPERLESS_DBDIR",
                os.path.join(BASE_DIR, "..", "data")
            ),
            "db.sqlite3"
        )
    }
}

if os.getenv("PAPERLESS_DBUSER"):
    DATABASES["default"] = {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": os.getenv("PAPERLESS_DBNAME", "paperless"),
        "USER": os.getenv("PAPERLESS_DBUSER"),
    }
    if os.getenv("PAPERLESS_DBPASS"):
        DATABASES["default"]["PASSWORD"] = os.getenv("PAPERLESS_DBPASS")
    if os.getenv("PAPERLESS_DBHOST"):
        DATABASES["default"]["HOST"] = os.getenv("PAPERLESS_DBHOST")
    if os.getenv("PAPERLESS_DBPORT"):
        DATABASES["default"]["PORT"] = os.getenv("PAPERLESS_DBPORT")


# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/1.10/topics/i18n/

LANGUAGE_CODE = 'de'
TIME_ZONE = os.getenv("PAPERLESS_TIME_ZONE", "UTC")
USE_I18N = True
USE_L10N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/

STATIC_ROOT = os.getenv(
    "PAPERLESS_STATICDIR", os.path.join(BASE_DIR, "..", "static"))
MEDIA_ROOT = os.getenv(
    "PAPERLESS_MEDIADIR", os.path.join(BASE_DIR, "..", "media"))

STATIC_URL = os.getenv("PAPERLESS_STATIC_URL", "/static/")
MEDIA_URL = os.getenv("PAPERLESS_MEDIA_URL", "/media/")

LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/'

# Other

# Settings for django-bootstrap4
BOOTSTRAP4 = {
    "include_jquery": True,
}

# Disable Django's artificial limit on the number of form fields to submit at
# once.  This is a protection against overloading the server, but since this is
# a self-hosted sort of gig, the benefits of being able to mass-delete a tonne
# of log entries outweight the benefits of such a safeguard.

DATA_UPLOAD_MAX_NUMBER_FIELDS = None


# Paperless-specific stuff
# You shouldn't have to edit any of these values.  Rather, you can set these
# values in /etc/paperless.conf instead.
# ----------------------------------------------------------------------------

# Logging

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "consumer": {
            "class": "documents.loggers.PaperlessLogger",
        }
    },
    "loggers": {
        "documents": {
            "handlers": ["consumer"],
            "level": os.getenv("PAPERLESS_CONSUMER_LOG_LEVEL", "INFO"),
        },
    },
}


# The default language that tesseract will attempt to use when parsing
# documents.  It should be a 3-letter language code consistent with ISO 639.
OCR_LANGUAGE = os.getenv("PAPERLESS_OCR_LANGUAGE", "eng")

# The amount of threads to use for OCR
OCR_THREADS = os.getenv("PAPERLESS_OCR_THREADS")

# OCR all documents?
OCR_ALWAYS = __get_boolean("PAPERLESS_OCR_ALWAYS")

# If this is true, any failed attempts to OCR a PDF will result in the PDF
# being indexed anyway, with whatever we could get.  If it's False, the file
# will simply be left in the CONSUMPTION_DIR.
FORGIVING_OCR = __get_boolean("PAPERLESS_FORGIVING_OCR")

# GNUPG needs a home directory for some reason
GNUPG_HOME = os.getenv("HOME", "/tmp")
GNUPG_BINARY = os.getenv("GNUPG_BINARY", "/usr/local/opt/gnupg/bin/gpg")

# Convert is part of the ImageMagick package
CONVERT_BINARY = os.getenv("PAPERLESS_CONVERT_BINARY", "convert")
CONVERT_TMPDIR = os.getenv("PAPERLESS_CONVERT_TMPDIR")
CONVERT_MEMORY_LIMIT = os.getenv("PAPERLESS_CONVERT_MEMORY_LIMIT")
CONVERT_DENSITY = os.getenv("PAPERLESS_CONVERT_DENSITY")

# Ghostscript
GS_BINARY = os.getenv("PAPERLESS_GS_BINARY", "gs")

# OptiPNG
OPTIPNG_BINARY = os.getenv("PAPERLESS_OPTIPNG_BINARY", "optipng")

# Unpaper
UNPAPER_BINARY = os.getenv("PAPERLESS_UNPAPER_BINARY", "unpaper")

# This will be created if it doesn't exist
SCRATCH_DIR = os.getenv("PAPERLESS_SCRATCH_DIR", "/tmp/paperless")

# This is where Paperless will look for PDFs to index
CONSUMPTION_DIR = os.getenv("PAPERLESS_CONSUMPTION_DIR")

# (This setting is ignored on Linux where inotify is used instead of a
# polling loop.)
# The number of seconds that Paperless will wait between checking
# CONSUMPTION_DIR.  If you tend to write documents to this directory very
# slowly, you may want to use a higher value than the default.
CONSUMER_LOOP_TIME = int(os.getenv("PAPERLESS_CONSUMER_LOOP_TIME", 10))

# Pre-2.x versions of Paperless stored your documents locally with GPG
# encryption, but that is no longer the default.  This behaviour is still
# available, but it must be explicitly enabled by setting
# `PAPERLESS_PASSPHRASE` in your environment or config file.  The default is to
# store these files unencrypted.
#
# Translation:
# * If you're a new user, you can safely ignore this setting.
# * If you're upgrading from 1.x, this must be set, OR you can run
#   `./manage.py change_storage_type gpg unencrypted` to decrypt your files,
#   after which you can unset this value.
PASSPHRASE = os.getenv("PAPERLESS_PASSPHRASE")

# Trigger a script after every successful document consumption?
PRE_CONSUME_SCRIPT = os.getenv("PAPERLESS_PRE_CONSUME_SCRIPT")
POST_CONSUME_SCRIPT = os.getenv("PAPERLESS_POST_CONSUME_SCRIPT")

# Whether to display a selected document inline, or download it as attachment:
INLINE_DOC = __get_boolean("PAPERLESS_INLINE_DOC")

# The number of items on each page in the web UI.  This value must be a
# positive integer, but if you don't define one in paperless.conf, a default of
# 100 will be used.
PAPERLESS_LIST_PER_PAGE = int(os.getenv("PAPERLESS_LIST_PER_PAGE", 100))

FY_START = os.getenv("PAPERLESS_FINANCIAL_YEAR_START")
FY_END = os.getenv("PAPERLESS_FINANCIAL_YEAR_END")

# Specify the default date order (for autodetected dates)
DATE_ORDER = os.getenv("PAPERLESS_DATE_ORDER", "DMY")
FILENAME_DATE_ORDER = os.getenv("PAPERLESS_FILENAME_DATE_ORDER")

# Transformations applied before filename parsing
FILENAME_PARSE_TRANSFORMS = []
for t in json.loads(os.getenv("PAPERLESS_FILENAME_PARSE_TRANSFORMS", "[]")):
    FILENAME_PARSE_TRANSFORMS.append((re.compile(t["pattern"]), t["repl"]))

# Specify for how many years a correspondent is considered recent. Recent
# correspondents will be shown in a separate "Recent correspondents" filter as
# well. Set to 0 to disable this filter.
PAPERLESS_RECENT_CORRESPONDENT_YEARS = int(os.getenv(
    "PAPERLESS_RECENT_CORRESPONDENT_YEARS", 0))

# Specify the filename format for out files
PAPERLESS_FILENAME_FORMAT = os.getenv("PAPERLESS_FILENAME_FORMAT")
