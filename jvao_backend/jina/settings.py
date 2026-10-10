"""
Django settings for the jina project (Django 3.2).

Docs:
    Settings overview  https://docs.djangoproject.com/en/3.2/topics/settings/
    Settings reference https://docs.djangoproject.com/en/3.2/ref/settings/
"""

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent


# ──────────────────────────────────────────────────────────────
#  Core
# ──────────────────────────────────────────────────────────────

# WARNING: keep the production secret key out of source control.
SECRET_KEY = "django-insecure-2!w#&@$kc02q2nefwjqchd5)dt3y1du3=4iujknnrmc=c!ybpc"

# WARNING: never run with DEBUG on in production.
DEBUG = True

ALLOWED_HOSTS = []

ROOT_URLCONF = "jina.urls"
WSGI_APPLICATION = "jina.wsgi.application"
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# ──────────────────────────────────────────────────────────────
#  Applications
# ──────────────────────────────────────────────────────────────

INSTALLED_APPS = [
    # Third-party
    "corsheaders",
    "rest_framework",
    "import_export",

    # Local
    "jinaapp.apps.JinaappConfig",

    # Django
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]


# ──────────────────────────────────────────────────────────────
#  Templates
# ──────────────────────────────────────────────────────────────

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "jinaapp" / "templates"],
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


# ──────────────────────────────────────────────────────────────
#  Database
# ──────────────────────────────────────────────────────────────

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    },
}


# ──────────────────────────────────────────────────────────────
#  Authentication
# ──────────────────────────────────────────────────────────────

_VALIDATORS = "django.contrib.auth.password_validation"

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": f"{_VALIDATORS}.UserAttributeSimilarityValidator"},
    {"NAME": f"{_VALIDATORS}.MinimumLengthValidator"},
    {"NAME": f"{_VALIDATORS}.CommonPasswordValidator"},
    {"NAME": f"{_VALIDATORS}.NumericPasswordValidator"},
]


# ──────────────────────────────────────────────────────────────
#  Internationalization
# ──────────────────────────────────────────────────────────────

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"

USE_I18N = True
USE_L10N = True
USE_TZ = True


# ──────────────────────────────────────────────────────────────
#  Static files
# ──────────────────────────────────────────────────────────────

STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "jinaapp" / "static"]


# ──────────────────────────────────────────────────────────────
#  Third-party packages
# ──────────────────────────────────────────────────────────────

# django-cors-headers
CORS_ORIGIN_ALLOW_ALL = True

# django-import-export
IMPORT_EXPORT_USE_TRANSACTIONS = True
