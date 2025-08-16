import os
from django.db import models
from pathlib import Path
from dotenv import load_dotenv
load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", "dev-default-key")
DEBUG = os.getenv("DEBUG", "True").lower() == "true"

CSRF_TRUSTED_ORIGINS = os.getenv("CSRF_TRUSTED_ORIGINS", "http://127.0.0.1:8000,http://localhost:8000").split(",")

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.SessionAuthentication",
        "rest_framework.authentication.BasicAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": ["rest_framework.permissions.IsAuthenticated"],
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 25,
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
}

DATA_UPLOAD_MAX_MEMORY_SIZE = 10 * 1024 * 1024  # 10 MB
FILE_UPLOAD_MAX_MEMORY_SIZE = 10 * 1024 * 1024

INSTALLED_APPS = [
    'grappelli',               # <-- must be first!
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "drf_spectacular",
    "core",  # your main app
]

# Storacha feature flag and config
STORACHA_ENABLED = os.getenv("STORACHA_ENABLED", "False").lower() == "true"
STORACHA_ENDPOINT = os.getenv("STORACHA_ENDPOINT", "")
STORACHA_API_KEY = os.getenv("STORACHA_API_KEY", "")

STORAGES = {
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage"
    }
}

SPECTACULAR_SETTINGS = {
    "TITLE": "IAmHub API",
    "DESCRIPTION": "Decentralized sovereignty hub APIs",
    "VERSION": "1.0.0",
}

# --- Shareable stamp links (stateless, HMAC) ---
FEATURE_SHARE_STAMP = os.getenv("FEATURE_SHARE_STAMP", "True").lower() == "true"            # flip to False to disable instantly
SHARELINK_TTL_SECONDS = 60 * 60       # 1 hour TTL

# --- Email basics ---
EMAIL_BACKEND = os.getenv("EMAIL_BACKEND", "django.core.mail.backends.console.EmailBackend")
DEFAULT_FROM_EMAIL = os.getenv("DEFAULT_FROM_EMAIL", "no-reply@iamhub.net")
SITE_URL = os.getenv("SITE_URL", "http://127.0.0.1:8000")
ADMINS_EMAIL = os.getenv("ADMINS_EMAIL", "")

ADMINS = [("Admin", os.getenv("ADMINS_EMAIL", ""))] if os.getenv("ADMINS_EMAIL") else []

# receipts
FEATURE_EMAIL_RECEIPTS = os.getenv("FEATURE_EMAIL_RECEIPTS", "True").lower() == "true"
FEATURE_VERIFICATION_EMAILS = True

INTERNAL_CRON_TOKEN = os.getenv("INTERNAL_CRON_TOKEN", "")

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
            ],
        },
    },
]

SECURE_HSTS_SECONDS = int(os.getenv("SECURE_HSTS_SECONDS", "60"))  # Start low, raise after confirming HTTPS
SECURE_HSTS_INCLUDE_SUBDOMAINS = os.getenv("SECURE_HSTS_INCLUDE_SUBDOMAINS", "True").lower() == "true"
SECURE_HSTS_PRELOAD = os.getenv("SECURE_HSTS_PRELOAD", "False").lower() == "true"
SECURE_SSL_REDIRECT = os.getenv("SECURE_SSL_REDIRECT", "True").lower() == "true"
SESSION_COOKIE_SECURE = os.getenv("SESSION_COOKIE_SECURE", "True").lower() == "true"
CSRF_COOKIE_SECURE = os.getenv("CSRF_COOKIE_SECURE", "True").lower() == "true"
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "localhost,127.0.0.1").split(",")
print("ALLOWED_HOSTS:", ALLOWED_HOSTS)

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"